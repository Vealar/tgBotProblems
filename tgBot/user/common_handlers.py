from aiogram import Bot, Dispatcher, types
from aiogram import types, Router
from db.models.models import User
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from db.repositories.database import db
from db.services.service_user import ServiceUser

router_common = Router()
service = ServiceUser()


@router_common.message(Command('help'))
async def help_command(message: types.Message):
    """Отправка справки"""
    help_text = "Доступные команды:\n" \
                "/start - Начало диалога с ботом\n" \
                "/help - Получить справку о доступных командах\n" \
                "/search - Найти нужную задачу\n" \
                "/reset - Сделать все задачи нерешенные\n" \
                "/show_solved - Показать все решенные задачи \n" \
                "/admin - Войти как админ\n"
    await message.answer(help_text)


@router_common.message(Command('reset'))
async def reset(message: types.Message):
    a = message.from_user.id
    service.reset_user_history(message.from_user.id)
    await message.answer("Теперь все задачи нерешенные")


@router_common.message(Command('show_solved'))
async def show_solved(message: types.Message):
    id = int(message.from_user.id)
    session = db.session()
    with session:
        user = session.query(User).filter_by(id=id).first()
        if user:
            result = service.get_solved_problems(id)
            if result:
                for i in result:
                    await message.answer(str(i))
            else:
                await message.answer('Вы не решили задачи')
        else:
            await message.answer("Вы не зарегистрированы. Начните с команды /start.")