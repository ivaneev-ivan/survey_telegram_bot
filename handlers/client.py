from aiogram import types, Dispatcher
from aiogram.dispatcher import filters

from create_bot import bot
from key_boards import kb_client


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что изволите, хозяин?', reply_markup=kb_client)


# @dp.message_handler(commands=['help'])
async def show_help_text(message: types.Message):
    await bot.send_message(message.from_user.id, '''Данный бот предназначен для повторения часто встречающихся вопросов на собеседовании по теме "Тестирование программного продукта". 
По нажатию кнопки "Получить вопросы" бот отправит вопросы  и ответы на них. Нажав на кнопку "Загрузить свой вопрос", можно загрузить вопрос с ответом для пополнения базы знаний бот ''',
                           reply_markup=kb_client)


# @dp.register_message_handler(commands=['get_questions_and_answers'])
async def get_questions_and_answers(message: types.Message):
    await bot.send_message(message.from_user.id, "Получить вопросы", reply_markup=kb_client)





def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(show_help_text, commands=['help'])
    dp.register_message_handler(show_help_text, filters.Text(equals=['Помощь']))
    dp.register_message_handler(get_questions_and_answers, filters.Text(equals=['Получить вопросы и ответы']))

