from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup)

keyboard_search = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать все задачи",callback_data="show_all")],
    [InlineKeyboardButton(text="Выбрать тему задач",callback_data="show_topic")],
    [InlineKeyboardButton(text="Выбрать уровень задач",callback_data="show_level")],
    [InlineKeyboardButton(text="Показать задачу по id",callback_data="show_id")],
    [InlineKeyboardButton(text="Выбрать уровень и тему задач",callback_data="show_topic_level")],

])
keyboard_level = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1",callback_data="EASY")],
    [InlineKeyboardButton(text="2",callback_data="MIDDLE")],
    [InlineKeyboardButton(text="3",callback_data="HARD")],
    [InlineKeyboardButton(text="4",callback_data="COFFIN")]
])
keyboard_one_problem = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать задачу", callback_data="show_task")],
    [InlineKeyboardButton(text="Показать решение",callback_data="show_solution")],
    [InlineKeyboardButton(text="Отметить решенной",callback_data="now_solved")],
    [InlineKeyboardButton(text="Отметить нерешенной",callback_data="now_not_solved")],
])
keyboard_admin_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить задачу",callback_data="admin_add_problem")],
    [InlineKeyboardButton(text="Удалить задачу",callback_data="admin_delete_problem")],
    [InlineKeyboardButton(text="Изменить задачу",callback_data="admin_change_problem")],
    [InlineKeyboardButton(text="Изменить темы задачи",callback_data="admin_change_topic")]
])
keyboard_admin_task_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить описание",callback_data="admin_change_description")],
    [InlineKeyboardButton(text="Изменить решение",callback_data="admin_change_solution")],
    [InlineKeyboardButton(text="Изменить уровень",callback_data="admin_change_level")],
])
keyboard_admin_topic_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить темы к задаче",callback_data="admin_add_topics")],
    [InlineKeyboardButton(text="Удалить темы к задаче",callback_data="admin_delete_topics")],
])


