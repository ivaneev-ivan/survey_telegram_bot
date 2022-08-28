import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api import get_questions, get_data_by_id
from create_bot import bot
from create_bot import dp
from key_boards import kb_client


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что изволите, хозяин?', reply_markup=kb_client)


# @dp.message_handler(commands=['help'])
async def show_help_text(message: types.Message):
    await bot.send_message(message.from_user.id, '''Данный бот предназначен для повторения часто встречающихся вопросов на собеседовании по теме "Тестирование программного продукта". 
По нажатию кнопки "Получить вопросы" бот отправит вопросы  и ответы на них. Нажав на кнопку "Загрузить свой вопрос", можно загрузить вопрос с ответом для пополнения базы знаний бот '''
                           )


# @dp.register_message_handler(commands=['get_questions_and_answers'])
async def get_questions_and_answers(message: types.Message):
    all_questions = await get_questions()
    new_list = random.sample(all_questions, 5)
    for question in new_list:
        await bot.send_message(message.from_user.id, f'{question["title"]}', reply_markup=InlineKeyboardMarkup(resize_keyboard=True). \
                               add(
            InlineKeyboardButton('Посмотреть ответ', callback_data=f'show_answer {question["id"]}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('show_answer'))
async def show_answer(call: types.CallbackQuery):
    print(call.message)
    data = await get_data_by_id(int(call.data.strip('show_answer ')))
    # await bot.send_message(call.message.from_user.id, data['answer'], reply_to_message_id=call.inline_message_id)
    await call.message.edit_text(f'Вопрос: \n*{data["title"]}*\n**Ответ:** \n_{data["answer"]}_', parse_mode='Markdown')

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(show_help_text, commands=['help'])
    dp.register_message_handler(show_help_text, filters.Text(equals=['Помощь']))
    dp.register_message_handler(get_questions_and_answers, filters.Text(equals=['Получить вопросы и ответы']))
