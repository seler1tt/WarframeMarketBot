# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data.config import BOT_VERSION, PATH_LOGS, PATH_DATABASE
from loader import dp
from utils.const_functions import get_date
from utils.misc.bot_filters import IsAdmin


# Получение БД
@dp.message_handler(IsAdmin(), commands=['db', 'database'], state="*")
async def admin_database(message: Message, state: FSMContext):
    with open(PATH_DATABASE, "rb") as document:
        await message.answer_document(
            document,
            caption=f"<b>📦 BACKUP\n"
                    f"🕰 <code>{get_date()}</code></b>",
        )


# Получение Логов
@dp.message_handler(IsAdmin(), commands=['log', 'logs'], state="*")
async def admin_log(message: Message, state: FSMContext):
    with open(PATH_LOGS, "rb") as document:
        await message.answer_document(
            document,
            caption=f"<b>🖨 LOGS\n"
                    f"🕰 <code>{get_date()}</code></b>",
        )