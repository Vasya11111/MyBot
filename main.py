
import asyncio
import logging
import time
import datetime
from datetime import timedelta
import aiogram.utils.markdown as md
import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ContentType
from aiogram.utils import executor

dict_sample = {
    "startdate": datetime.datetime.now(),
    "users": [916199890],
    "messages": [(1, 'message1 <a href="https://google.com/">ссылка1</a>') ,(2,'message2 <a href="https://google.com/">ссылка2</a>') ,(3, 'message3 <a href="https://google.com/">ссылка3</a>') ,(4, 'message4 <a href="https://google.com/">ссылка4</a>')],
    "description": "Это лендинговый курс, который ...."

}

chatslist= {}
chatslist["-947416346"]=dict_sample

dict_sample = {
    "startdate": datetime.datetime.now(),
    "users": [916199890,5646589895],
    "messages": [(1, 'message1anotherCourse <a href="https://google.com/">ссылка1</a>') ,(2,'message2anotherCourse <a href="https://google.com/">ссылка2</a>') ,(3, 'message3anotherCourse <a href="https://google.com/">ссылка3</a>') ],
    "description": "Это другой лендинговый курс, который ...."

}
chatslist["-985007997"]=dict_sample



dict_sample = {
    "startdate": datetime.datetime.now(),
    "users": [916199890],
    "messages": [(1, 'privateMessage1 <a href="https://google.com/">ссылка1</a>') ,(2,'privateMessage2 <a href="https://google.com/">ссылка2</a>') ,(3, 'privateMessage3 <a href="https://google.com/">ссылка3</a>') ],
    "description": "Это private лендинговый курс, который ...."

}
chatslist["916199890"]=dict_sample

# user_id=916199890(main) 5646589895
# chat_id=-947416346 - 1
# chat_id=-985007997 - 2


logging.basicConfig(level=logging.INFO)

API_TOKEN = '6372592967:AAEp6c2eoyspJBvzRYevsi4ZzrKTIea5cXw'


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# @dp.message_handler()
# async def func(message: types.Message):
#     await bot.send_message(message.chat.id, message.chat.id)


async def on_startup(_):
    asyncio.create_task(scheduler())

async def noon_print(args):
    await bot.send_message(args[0], args[1],parse_mode="HTML")

async def scheduler():
    for key,sample in chatslist.items():
        for i in sample["messages"]:
            time = dict_sample["startdate"] + timedelta(minutes=i[0])
            aioschedule.every().day.at(time.strftime("%H:%M")).do(noon_print, args=(key,i[1]))

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def on_chat_member(message: types.Message):
    if(chatslist[str(message.chat.id)]["users"].count(message.from_user.id)==0):
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)



@dp.message_handler(commands='about')
async def func(message: types.Message):
    await bot.send_message(message.chat.id,chatslist[str(message.chat.id)]["description"])


@dp.message_handler(commands='history')
async def func(message: types.Message):
    currentTime = datetime.datetime.now()
    for i in chatslist[str(message.chat.id)]["messages"]:
        if (currentTime > (chatslist[str(message.chat.id)]["startdate"] + timedelta(minutes=i[0]))):
            await bot.send_message(message.chat.id, i[1],parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)


