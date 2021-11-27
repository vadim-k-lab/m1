import os
from aiogram.dispatcher.filters import state
from exelpars import databut, datasort, dicsort
from aiogram import Bot, Dispatcher, executor, types, filters
from decouple import config
import command
import command2
from user import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# FUNC #
fun = {'каталог':command.catalog, 'акции':command.action, 'корзина':command.shoppack}

# WH(1part)
WEBHOOK_HOST = 'https://depbot2.herokuapp.com'  # name your app
#WEBHOOK_HOST = 'http://127.0.0.1'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT', 5000)
#TOKEN = os.environ['TOKEN']


bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
#users = {}# потом сделать запись в базу юзеров чтоб не потерять

# START #
@dp.message_handler(filters.CommandStart())
async def command_start_handler(msg):
    await command.startans(dp, msg)

# HELP #
@dp.message_handler(filters.CommandHelp())
async def bot_help(msg: types.message):
    await command2.help(bot, msg)

# CATALOG #
@dp.message_handler(commands=['catalog', 'shop'])
async def catalog_set(msg):
    if msg.text == '/shop':
        await callback(bot, msg, 'корзина')
    else:
        await command.catalog(dp.bot, msg, dicsort)

@dp.message_handler(commands=['test', 'cansel', 'log'])
async def testans(msg):
    await command2.test(bot, msg)

@dp.message_handler(text = ["каталог", "акции", "корзина", "история"])
async def text_in_handler(msg):
    await callback(bot, msg, msg.text)

# Buttonlink Startpack #
@dp.callback_query_handler(lambda c: c.data in ["каталог", "акции", "корзина", "история"])
async def process_callback(query):
    await callback(bot, query.message, query.data)

@dp.callback_query_handler(lambda c: c.data in ["галерея", "информация", "стоимость", "назад"])
async def process_callback(query):
    await command.calledit(bot, query)

@dp.callback_query_handler(lambda c: c.data in ["экстра", "1й разбор", "2й разбор", "3й разбор", "детки"])
async def process_callback(query):
    await command.calledit2(bot, query)

@dp.callback_query_handler(lambda c: c.data in ["+1", "+2", "+5", "+10", "-1", "-2", "-5", "-10", "вернуться", "сбросить", "в корзину"])
async def process_callback(query):
    await command.calledit3(bot, query)

@dp.callback_query_handler(lambda c: c.data == "в корзину1")
async def process_callback(query):
    await command.shopping(bot, query.message, dicsort)

@dp.callback_query_handler(lambda c: c.data in ["удалить"])
async def process_callback(query):
    await command.delpack(bot, query.message)

@dp.callback_query_handler(lambda c: c.data == "заказать")
async def process_callback(query):
    await command.ordpack(bot, query.message)

@dp.message_handler(content_types=types.ContentType.CONTACT) # контакт юзера
async def test(msg):
    await command.contact(bot, msg)

# CALLBACK_LOGIC #
async def callback(bot, msg, data):
    if data in fun:
        await fun[data](bot, msg, dicsort)
    else:
        await bot.send_message(msg.chat.id, f'Нажата кнопка {data}!')

#POLLING
#executor.start_polling(dp, skip_updates=True)

# WH(2part)
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
                  #int(os.environ.get('PORT', 5000)))