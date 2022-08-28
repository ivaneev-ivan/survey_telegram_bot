from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text
from key_boards.client_kb import kb_client
from api import set_questions


from create_bot import dp, bot
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class FSMAddQuestion(StatesGroup):
    question = State()
    answer = State()


# Начало диалога о загрузки вопроса и ответа
# @dp.register_message_handler(filters.Text(equals=['Добавить вопросы и ответы']),state=None)
async def set_questions_and_answers(message: types.Message):
    await bot.send_message(message.from_user.id,'Загрузите свой вопрос', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Отменить', callback_data='cancel')))
    await FSMAddQuestion.question.set()


@dp.callback_query_handler(text="cancel",state='*')
async def cancel_callback(call:types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await call.message.reply('Загрузка отменена')



# Запись вопроса пользователя
# @dp.message_handler(state=FSMAddQuestion.question)
async  def load_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
        data['user_id'] = message.from_user.id
    await FSMAddQuestion.next()
    await message.reply('Загрузите ответ на свой вопрос')


# Запись вопроса пользователя
# @dp.message_handler(state=FSMAddQuestion.answer)
async def load_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
        status = await set_questions(data['question'],data['answer'],data['user_id'])
        print(status)
    await state.finish()


# Регистрация handler
def register_handler(dp:Dispatcher):
    dp.register_message_handler(set_questions_and_answers, filters.Text(equals=['Добавить вопросы и ответы']),
                                state=None)
    dp.register_message_handler(load_question, state=FSMAddQuestion.question)
    dp.register_message_handler(load_answer, state=FSMAddQuestion.answer)

