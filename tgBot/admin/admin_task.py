from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.types import CallbackQuery

from db.models.models import Admin
from db.repositories.database import db
from db.services.service_admin import ServiceAdmin
from aiogram import types, Router, F
from db.models.models import Problem
from tgBot.registration.registration_handlers import Registration
from tgBot.keyboard.keyboard import keyboard_admin_task_change,keyboard_admin_topic_change,keyboard_admin_setting
router_admin = Router()
service = ServiceAdmin()


class Admin_State (StatesGroup):
    task_add = State()

    task_delete = State()

    task_change_description = State()
    task_change_level = State()
    task_change_solution = State()

    task_add_topic = State()
    task_delete_topic = State()



@router_admin.message(Command("setting"))
async def setting(message: types.Message,state:FSMContext):
    """Функционал админа по задачам"""
    user_id = message.from_user.id
    session = db.session()
    admin = session.query(Admin).filter_by(user_id=user_id).first()
    if admin:
        await message.answer("Выберите, что необходимо сделать с задачей",reply_markup=keyboard_admin_setting)
    else:
        await message.answer(f"У вас нет прав, выполнять эту комманду, если вы являетесь "
                             f"администратором, то введите свой персональный ключ"
                             f" /admin")




@router_admin.callback_query(F.data == 'admin_add_problem')
async def admin_add_problem(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {Level\Description\Solving}')
    await state.set_state(Admin_State.task_add)
@router_admin.message(Admin_State.task_add)
async def add_problem_second(message:types.Message,state:FSMContext):
    try:
        level, description, solving = message.text.split('\\')
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: Level\\Description\\Solving")
        return
    service.add_problem(level,description,solving)
    # Отправляем ответ пользователю
    await message.answer(f"Задача добавлена")
    # Очистка состояния
    await state.clear()




@router_admin.callback_query(F.data == 'admin_delete_problem')
async def admin_delete_problem(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id_problem}')
    await state.set_state(Admin_State.task_delete)
@router_admin.message(Admin_State.task_delete)
async def delete_problem_second(message:types.Message,state:FSMContext):
    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: Level\\Description\\Solving")
        return
    service.delete_problem(id)
    # Отправляем ответ пользователю
    await message.answer(f"Задача удалена")
    # Очистка состояния
    await state.clear()




@router_admin.callback_query(F.data == 'admin_change_problem')
async def admin_change_problem(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text('Выберите что хотите поменять у задачи',reply_markup = keyboard_admin_task_change)


@router_admin.callback_query(F.data == 'admin_change_description')
async def admin_change_description(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id_problem\description}')
    await state.set_state(Admin_State.task_change_description)
@router_admin.callback_query(F.data == 'admin_change_solution')
async def admin_change_solution(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id_problem\solution}')
    await state.set_state(Admin_State.task_change_solution)
@router_admin.callback_query(F.data == 'admin_change_level')
async def admin_change_level(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id_problem\level}')
    await state.set_state(Admin_State.task_change_level)




@router_admin.message(Admin_State.task_change_description)
async def change_problem_second(message:types.Message,state:FSMContext):
    try:
        id,description = message.text.split('\\')
        id = int(id)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: Level\\Description\\Solving")
        return
    service.update_problem_description(id,description)
    # Отправляем ответ пользователю
    await message.answer(f"Описание изменено")
    # Очистка состояния
    await state.clear()
@router_admin.message(Admin_State.task_change_solution)
async def change_problem_second(message:types.Message,state:FSMContext):
    try:
        id,solution = message.text.split('\\')
        id = int(id)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: Level\\Description\\Solving")
        return
    service.update_problem_solution(id,solution)
    # Отправляем ответ пользователю
    await message.answer(f"Решение изменено")
    # Очистка состояния
    await state.clear()
@router_admin.message(Admin_State.task_change_level)
async def change_problem_second(message:types.Message,state:FSMContext):
    try:
        id,level = message.text.split('\\')
        id = int(id)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: Level\\Description\\Solving")
        return
    service.update_problem_level(id,level)
    # Отправляем ответ пользователю
    await message.answer(f"Сложность изменена")
    # Очистка состояния
    await state.clear()



@router_admin.callback_query(F.data == 'admin_change_topic')
async def admin_change_topic(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text('Выберите что хотите сделать с темами задачи',reply_markup = keyboard_admin_topic_change)




@router_admin.callback_query(F.data == 'admin_add_topics')
async def admin_change_description(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите темы в формате {id\\topic1\\topic2...\\}')
    await state.set_state(Admin_State.task_add_topic)
@router_admin.callback_query(F.data == 'admin_delete_topics')
async def admin_change_description(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите темы в формате {id\\topic1\\topic2...\\}')
    await state.set_state(Admin_State.task_delete_topic)




@router_admin.message(Admin_State.task_add_topic)
async def add_topic_second(message:types.Message,state:FSMContext):
    try:
        topics = message.text.split('\\')
        id = int(topics[0])
        topics = topics[1:]
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: id\\topic1\\topic2...\\")
        return
    service.add_topics_to_problem(id,topics)
    # Отправляем ответ пользователю
    await message.answer(f"Темы добавлена")
    # Очистка состояния
    await state.clear()
@router_admin.message(Admin_State.task_delete_topic)
async def delete_topic_second(message:types.Message,state:FSMContext):
    try:
        topics = message.text.split('\\')
        id = int(topics[0])
        topics = topics[1:]
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: id\\topic1\\topic2...\\")
        return
    service.remove_topics_from_problem(id,topics)
    # Отправляем ответ пользователю
    await message.answer(f"Темы удалены")
    # Очистка состояния
    await state.clear()
