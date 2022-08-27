from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text
from key_boards.client_kb import kb_client


from create_bot import dp, bot
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAddQuestion(StatesGroup):
    question = State()
    answer = State()


# Начало диалога о загрузки вопроса и ответа
# @dp.register_message_handler(filters.Text(equals=['Добавить вопросы и ответы']),state=None)
async def set_questions_and_answers(message: types.Message):
    await bot.send_message(message.from_user.id,'Загрузите свой вопрос', reply_markup=kb_client)
    await FSMAddQuestion.question.set()



# Выход по кнопке "Отмена" из машинного состояния
# @dp.message_handler(state='*',commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# Запись вопроса пользователя
# @dp.message_handler(state=FSMAddQuestion.question)
async  def load_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await FSMAddQuestion.next()
    await message.reply('Загрузите ответ на свой вопрос')


# Запись вопроса пользователя
# @dp.message_handler(state=FSMAddQuestion.answer)
async  def load_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
    # TODO Запись данных пользователя в БД
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()


# Регистрация handler
def register_handler(dp:Dispatcher):
    dp.register_message_handler(set_questions_and_answers, filters.Text(equals=['Добавить вопросы и ответы']),
                                state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_question, state=FSMAddQuestion.question)
    dp.register_message_handler(load_answer, state=FSMAddQuestion.answer)

