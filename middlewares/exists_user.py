# - *- coding: utf- 8 - *-
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update

from services.api_sqlite import get_userx, update_userx, add_userx


# Проверка юзеров в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def on_process_update(self, update: Update, data: dict):
        if "message" in update:
            this_user = update.message.from_user
        elif "callback_query" in update:
            this_user = update.callback_query.from_user
        else:
            this_user = None

        if this_user is not None and not this_user.is_bot:
            get_user = get_userx(user_id=this_user.id)
            user_login = (this_user.username or "").lower()

            if get_user is None:
                add_userx(user_id=this_user.id, user_login=user_login)
            elif user_login != get_user['user_login']:
                update_userx(this_user.id, user_login=user_login)
