# - *- coding: utf- 8 - *-
import os
import sys

from aiogram import executor, Dispatcher
import colorama

from handler import dp
from data.config import get_admins
from services.api_sqlite import create_dbx
from utils.misc.bot_logging import bot_logger
from utils.misc_functions import on_startup_notify, autobackup_admin
from middlewares import setup_middlewares
from utils.misc.bot_filters import IsPrivate
from loader import scheduler

colorama.init()

# Запуск шедулеров
async def scheduler_start():
    scheduler.add_job(autobackup_admin, trigger="cron", hour=00)

# Выполнение функции после запуска бота
async def on_startup(dp: Dispatcher):

    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)
    await scheduler_start()
    await on_startup_notify(dp)


    bot_logger.warning("BOT WAS STARTED")
    print(colorama.Fore.LIGHTYELLOW_EX + "~~~~~ Bot was started ~~~~~")
    print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ Bot created by @seler1tt ~~~~~")
    print(colorama.Fore.RESET)


    if len(get_admins()) == 0: print("***** ENTER ADMIN ID IN settings.ini *****")


# Выполнение функции после выключения бота
async def on_shutdown(dp: Dispatcher):

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()


    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

if __name__ == '__main__':
    create_dbx()
    
    scheduler.start()
    dp.filters_factory.bind(IsPrivate)
    setup_middlewares(dp)

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
