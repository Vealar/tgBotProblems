from aiogram import Bot, Dispatcher, types
from aiogram import types, Router,F
from db.models.models import User
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from db.repositories.database import db
from db.services.service_user import ServiceUser
from tgBot.keyboard.keyboard import keyboard_search,keyboard_one_problem
from aiogram.types import CallbackQuery
router_search = Router()
service = ServiceUser()

class User_State (StatesGroup):
    task_topic = State()
    task_level = State()
    task_topic_level = State()

    task_id_task = State()
    task_id_solve = State()
    task_id_add = State()
    task_id_delete = State()

    task_show_solved = State()


@router_search.message(Command('search'))
async def search(message: types.Message):
    """Найти необходимую задачу"""
    user_id = message.from_user.id
    session = db.session()
    with session:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            await message.answer("Выбери параметры поиска", reply_markup=keyboard_search)
        else:
            await message.answer("Вы не зарегистрированы. Начните с команды /start.")

@router_search.callback_query(F.data == 'show_all')
async def show_all(callback:CallbackQuery):
    result = service.get_all_problems()
    if result:
        for i in result:
            await callback.message.answer(i)
    else:
        await callback.message.answer('База пустая, обратитесь к администарторам')




@router_search.callback_query(F.data == 'show_topic')
async def show_topic(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите нужные темы в формате topi1\\topic2\\topic3\\...')
    await state.set_state(User_State.task_topic)
@router_search.message(User_State.task_topic)
async def show_topic_second(message:types.Message,state:FSMContext):
    try:
        topics = message.text.split('\\')
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {topic}")
        return
    result = service.get_problem_by_topics(topics)
    if result:
        for i in result:
            await message.answer(f"{i}\n")
    else:
        await message.answer(f"Задач на эту тему нет")
    # Очистка состояния
    await state.clear()




@router_search.callback_query(F.data == 'show_level')
async def show_level(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text('Введите нужный уровень')
    await state.set_state(User_State.task_level)
@router_search.message(User_State.task_level)
async def show_level_second(message: types.Message, state: FSMContext):
    try:
        level = message.text
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.get_problem_by_level(level)
    if result:
        for i in result:
            await message.answer(f"{i}\n")
    else:
        await message.answer(f"Задач на эту сложность нет")
    # Очистка состояния
    await state.clear()


@router_search.callback_query(F.data == 'show_topic_level')
async def show_topic_level(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {Level\Topic}')
    await state.set_state(User_State.task_topic_level)
@router_search.message(User_State.task_topic_level)
async def show_topic_level_second(message: types.Message, state: FSMContext):
    try:
        level = message.text.split('\\')
        topics = level[1:]
        level = level[0]
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.get_problem_by_level_and_topics(level,topics)
    if result:
        for i in result:
            await message.answer(f"{i}\n")
    else:
        await message.answer(f"Задач на эту сложность нет")
    # Очистка состояния
    await state.clear()




@router_search.callback_query(F.data == 'show_id')
async def show_id(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Выберете что хотите сделать с задачей',reply_markup=keyboard_one_problem)

@router_search.callback_query(F.data == 'show_task')
async def show_task(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id}')
    await state.set_state(User_State.task_id_task)

@router_search.message(User_State.task_id_task)
async def show_task_second(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.get_problem_by_id(id)
    if result:
        await message.answer(result)
    else:
        await message.answer(f"Задача не найдена")
    # Очистка состояния
    await state.clear()

@router_search.callback_query(F.data == 'show_solution')
async def show_solution(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id}')
    await state.set_state(User_State.task_id_solve)

@router_search.message(User_State.task_id_solve)
async def show_solution_second(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.get_solve_by_id(id)
    if result:
        await message.answer(result)
    else:
        await message.answer(f"Задача не найдена")
    # Очистка состояния
    await state.clear()



@router_search.callback_query(F.data == 'now_solved')
async def now_solved(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id}')
    await state.set_state(User_State.task_id_add)

@router_search.message(User_State.task_id_add)
async def now_solved_second(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.add_solved_problem(message.from_user.id,id)
    if result:
        await message.answer("Задача отмечена решенной")
    else:
        await message.answer(f"Задача не найдена")
    # Очистка состояния
    await state.clear()




@router_search.callback_query(F.data == 'now_not_solved')
async def now_not_solved(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите данные о задаче в формате {id}')
    await state.set_state(User_State.task_id_delete)

@router_search.message(User_State.task_id_delete)
async def now_not_solved_second(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Ошибка формата! Пожалуйста, используйте формат: {level}")
        return
    result = service.delete_solved_problem(message.from_user.id,id)
    if result:
        await message.answer("Задача отмечена нерешенной")
    else:
        await message.answer(f"Задача не найдена")
    # Очистка состояния
    await state.clear()


