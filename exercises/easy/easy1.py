from routers import user_router
from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import tempfile
import sys
import subprocess

@user_router.callback_query(F.data == "Задача 1: print()")
async def exercise(cb:CallbackQuery, state:FSMContext):
    await state.set_state("task 1")
    await cb.message.answer('Напишіть програму яка виводить в консоль текст "I love Python!"')
    await cb.message.delete()

@user_router.message()
async def hello(message:Message):
    user_code = message.text
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(user_code.encode())
        filename = f.name
    
    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout)
    print(result.stderr)
    f.delete()
