from aiogram import Router
import filters
user_router = Router()
admin_router = Router()
user_tasks = Router()

user_router.message.filter(filters.UserFilter())
admin_router.message.filter(filters.AdminFilter())
