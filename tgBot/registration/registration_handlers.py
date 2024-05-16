from aiogram import types, Router
from db.models.models import User
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from db.repositories.database import db
from db.services.service_user import ServiceUser
router_registration = Router()
service = ServiceUser()


class Registration(StatesGroup):
    name = State()


@router_registration.message(Command("start"))
async def start(message: types.Message,state:FSMContext):
    """Начало диалога с ботом"""
    user_id = message.from_user.id
    session = db.session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        await message.answer("Привет! Я готов помочь тебе с математикой. "
                             "Используй /help для списка команд.")
        await message.answer("Как мне к вам обращаться? Напишите ваше имя, пожалуйста.")
        await state.set_state(Registration.name)
    else:
        await message.answer(f"Привет, {user.username}! Чем могу помочь?")


@router_registration.message(Registration.name)
async def start_second(message:types.Message,state:FSMContext):
    user = User(message.from_user.id,message.text)
    ServiceUser.add_user(user)
    await message.answer(f"Приятного решения задач,{message.text}")
    await state.clear()