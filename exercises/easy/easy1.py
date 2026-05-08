from routers import user_router



# @router.message(F.text == "ex")
# async def exercise(message:Message):
#     await message.answer('Напишіть програму яка виводить в консоль "Hello, World!"')

# @router.message()
# async def hello(message:Message):
#     user_code = message.text
#     with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
#         f.write(user_code.encode())
#         filename = f.name
    
#     result = subprocess.run(
#         ["python", filename],
#         capture_output=True,
#         text=True,
#         timeout=5
#     )
#     print(result.stdout)
#     print(result.stderr)
#     f.delete()
