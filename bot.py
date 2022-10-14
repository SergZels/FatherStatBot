from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from keyboards.client_keyboard import kbcl
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
#import os
from aiogram.dispatcher.middlewares import BaseMiddleware
from bd.bd import botBD
from loguru import logger
import conf
from aiogram.utils.executor import start_webhook

ADMIN_ID = conf.ADMIN_ID
# webhook settings
WEBHOOK_HOST = 'https://vmi957205.contaboserver.net'
WEBHOOK_PATH = '/prod_fatstat'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip 127.0.0.1
WEBAPP_PORT = 3003

Token = conf.TOKEN
bot = Bot(token=Token)#os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
botBD = botBD()
logger.add("debug.txt")

class FSMzap(StatesGroup):
    vuruhka = State()

class MidlWare(BaseMiddleware):
    async def on_process_update(self,update: types.Update,date: dict):
        #logger.debug(update)
        #logger.debug(update.message.from_user.id)
        if update.message.from_user.id not in ADMIN_ID:
            logger.debug(f"Хтось лівий зайшов {update.message.from_user.id}")
            raise CancelHandler()
  
@dp.message_handler(commands=['start', 'help'],state= None)
async def send_welcome(message: types.Message):
    await message.reply("Вітаю! Щоб розпочати натисніть кнопку внизу!",reply_markup=kbcl )

@dp.message_handler(commands=['Внести_виручку'],state=None)
async def echo(message : types.Message):
    await FSMzap.vuruhka.set()
    await message.answer("Напишіть вашу виручку:",reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=['Місяць'],state=None)
async def echo(message : types.Message):
    te=botBD.stat()
    doc = open('testplor.png', 'rb')
    await message.answer(te)
    await message.reply_photo(doc)
 
@dp.message_handler(content_types=[types.ContentType.TEXT],state=FSMzap.vuruhka)
async def get_pokaznik(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['viruhka'] = message.text
    logger.debug(f"Виручка - {message.text}")
    botBD.rec(data['viruhka'])
    await message.answer(f"Виручку {data['viruhka']}грн внесено!",reply_markup=kbcl)
    await state.finish()

@dp.message_handler()
async def echo(message : types.Message):
    if message.text == "Файл12":
        doc = open('debug.txt', 'rb')
        await message.reply_document(doc)
    else:
        await message.answer("Не розумію",reply_markup=kbcl)
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start
    logger.debug("Бот запущено")

async def on_shutdown(dp):
    logger.debug('Зупиняюся..')
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.debug('Бувай!')

if __name__ == '__main__':
    dp.middleware.setup(MidlWare())
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )   
#print("Bot running")

#executor.start_polling(dp,skip_updates=True)