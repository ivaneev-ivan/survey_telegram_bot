
from create_bot import dp
from aiogram.utils import executor
from handlers import client, loading_question



async def on_startup(_):
    print("Бот вышел в онлайн")

client.register_handler_client(dp)
loading_question.register_handler(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)