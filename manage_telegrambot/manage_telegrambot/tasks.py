from manage_telegrambot.celery import app
# from manage_telegrambot.utils import send


import asyncio
from aiogram import Bot, Dispatcher, types
from bots.models import Bot as Dj_Bot
from celery import shared_task


@shared_task
def run_bots():
    bots_objects = Dj_Bot.objects.all()
    bots = {}
    for bot_info in bots_objects:
        bot = Bot(token=bot_info.token)
        dp = Dispatcher(bot)
        bots[bot_info.name] = {'bot': bot, 'dp': dp}

    for bot_name, bot_data in bots.items():
        dp = bot_data['dp']
        @dp.message_handler(commands='start')
        async def start(message: types.Message):
            '''Функция выдающая ответ на команду start'''
            username = message.from_user['username']
            first_name = message.from_user['first_name']
            last_name = message.from_user['last_name']
            await message.answer(f'Hi, {username} ({first_name} {last_name})')

    # Запустите ботов
    for bot_name, bot_data in bots.items():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot_data['dp'].start_polling())
