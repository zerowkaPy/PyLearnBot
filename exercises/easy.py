from routers import user_tasks
from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

import tempfile
import os
import subprocess

import filters
from kb import user_kb

@user_tasks.message(F.text == "На головну")
async def menu_tasks(message:Message, state:FSMContext):
    await message.answer(
"""Ви повернулися на головну""",
reply_markup=user_kb.start
)
    await message.delete()
    await state.clear()


@user_tasks.callback_query(F.data == "Задача 1: print()")
async def ex1(cb:CallbackQuery, state:FSMContext):
    await state.set_state("task 1")
    await cb.message.answer('Напишіть програму яка виводить в консоль текст "I love Python!"', reply_markup=user_kb.menu)
    await cb.message.delete()

@user_tasks.message(filters.StateFilter("task 1"))
async def ex1_handler(message:Message, state:FSMContext):
    user_code = message.text
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(user_code.encode())
        f.close()
        filename = f.name
    
    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True,
        timeout=5)

    if result.stdout.strip().lower() != "i love python!":
        await message.answer("Щось пішло не так, спробуйте ще раз")
    else:
        await message.answer("Ви впорались!\nПочаток закладено - ви стали на один крок ближче до того щоб стати гуру Python 😎", reply_markup=user_kb.start)
        await state.clear()
            


@user_tasks.callback_query(F.data == "Задача 2: split()")
async def ex2(cb:CallbackQuery, state:FSMContext):
    await state.set_state("task 2")
    await cb.message.answer(
"""split() — це метод рядка, який розбиває текст на частини і повертає список
```python
text = "я люблю python"
print(text.split())
```
Результат буде:
```python
["я", "люблю", "python"]
```

У цього метода також є праметр sep, котрий вказує по яким символам буде розбиватися рядок:
```python
text = "яблуко, банан, апельсин"
print(text.split(", ")) #зверніть увагу що після коми стоїть пробіл
```
Результат буде:
```python
["яблуко", "банан", "апельсин"]
```
Якщо ви не вказуєете параметр sep, то автоматично здійснюється розбив рядка по пробілах, як це було в першому прикладі

Завдання:
Напишіть функцію subject яка приймає рядок, за допомогою метода split() розбиває його по символам ", " і віддає (return) список отриманих рядків
Виклик функції:
```python
print(subject("mathematics, physics, history, biology"))
```
Очікуваний результат:
```python
['mathematics','physics','history','biology']
```
""", parse_mode=ParseMode.MARKDOWN, reply_markup=user_kb.menu)
    await cb.message.delete()


@user_tasks.message(filters.StateFilter("task 2"))
async def ex2_handler(message:Message, state:FSMContext):
    user_code = message.text
    code = user_code+'\nprint(subject("mathematics, physics, history, biology"))'
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code.encode())
        f.close()
        filename = f.name
    
    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True,
        timeout=5)
    
    os.remove(filename)

    if result.stderr:
        error_lines = result.stderr.splitlines()
        filtered_error = "\n".join(line for line in error_lines if "File " not in line)
        await message.answer(f"В процесі виконання програми виникла помилка:\n{ filtered_error}")

    elif result.stdout.strip() != "['mathematics', 'physics', 'history', 'biology']":
        await message.answer(
f"""Ваш результат:
```
{result.stdout}
```
Очікуваний результат:
```
['mathematics', 'physics', 'history', 'biology']
```
Спробуйте ще раз""", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(
"""Ви виконали завдання, так тримати\\!
Результат:
> \\['mathematics', 'physics', 'history', 'biology'\\]""", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=user_kb.start)
        await state.clear()