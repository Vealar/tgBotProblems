from aiogram import types, Router
from db.models.models import User,Admin
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from db.repositories.database import db
from db.services.service_user import ServiceUser

router_registration_admin = Router()
service = ServiceUser()


class RegistrationAdmin(StatesGroup):
    name = State()


@router_registration_admin.message(Command("admin"))
async def admin(message: types.Message,state:FSMContext):
    """Начало диалога с ботом для админа"""
    user_id = message.from_user.id
    session = db.session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        await message.answer("Введите /start для начала работы")
    else:
        await message.answer(f"Введите свой персональный ключ админа")
        await state.set_state(RegistrationAdmin.name)


@router_registration_admin.message(RegistrationAdmin.name)
async def admin_second(message:types.Message,state:FSMContext):

    # Открываем сессию
    with db.session() as session:
        personal_key = int(message.text.strip())
        if isinstance(personal_key,int):
            # Проверяем, существует ли админ с данным персональным ключом
            admin = session.query(Admin).filter_by(id=personal_key).first()

            if admin:
                # Обновляем user_id для найденного админа
                admin.user_id = message.from_user.id
                session.commit()
                await message.answer(
                    f"Вы успешно зарегистрированы как админ. Приятного решения задач, {message.from_user.first_name}")
            else:
                await message.answer("Неверный персональный ключ. Попробуйте снова.")
        else:
            await message.answer("Неверный персональный ключ. Попробуйте снова.")

    # Очищаем состояние FSM
    await state.clear()