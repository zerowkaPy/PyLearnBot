from aiogram.filters.base import Filter
from aiogram.types import Message
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