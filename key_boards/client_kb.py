from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('Получить вопросы и ответы')
b2 = KeyboardButton('Добавить вопросы и ответы')
b3 = KeyboardButton('Помощь')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b3).row(b1,b2)