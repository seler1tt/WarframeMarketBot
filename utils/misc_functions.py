# - *- coding: utf- 8 - *-
from loader import bot
from aiogram import Dispatcher
from data.config import get_admins, BOT_DESCRIPTION, PATH_DATABASE
from utils.const_functions import get_date

# Уведомление при запуске бота
async def on_startup_notify(dp: Dispatcher):
    if len(get_admins()) >= 1:
        await send_admins(f"<b>✅ Бот был успешно запущен</b>\n"
                          f"➖➖➖➖➖➖➖➖➖➖\n"
                          f"{BOT_DESCRIPTION}\n"
                          f"➖➖➖➖➖➖➖➖➖➖\n"
                          f"<code>❗ Данное сообщение видят только администраторы бота.</code>")


# Рассылка сообщения всем администраторам
async def send_admins(message, not_me=0):
    for admin in get_admins():
        try:
            if str(admin) != str(not_me):
                await bot.send_message(admin, message, disable_web_page_preview=True)
        except:
            pass


# Автобэкапы БД для админов
async def autobackup_admin():
    for admin in get_admins():
        with open(PATH_DATABASE, "rb") as document:
            try:
                await bot.send_document(
                    admin,
                    document,
                    caption=f"<b>📦 AUTOBACKUP</b>\n"
                            f"🕰 <code>{get_date()}</code>",
                )
            except:
                pass
