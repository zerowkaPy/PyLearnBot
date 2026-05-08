from aiogram.filters.base import Filter
from aiogram.types import Message
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Update

import os

CREATOR_ID = int(os.getenv("CREATOR_ID")) #load_dotenv відбувається в main.py

class AdminFilter(Filter):
    def __init__(self):
        self.admin_id = CREATOR_ID
        
    async def __call__(self, message:Message):
        return self.admin_id == message.from_user.id
    
class UserFilter(Filter):
    def __init__(self):
        self.admin_id = CREATOR_ID

    async def __call__(self, message:Message):
        return self.admin_id != message.from_user.id

class StateFilter(Filter):
    def __init__(self, expected_state:str):
        self.expected_state = expected_state

    async def __call__(self, event:Update, state:FSMContext):
        current_state:str = await state.get_state()
        return self.expected_state == current_state