# - *- coding: utf- 8 - *-
from datetime import datetime

import pytz

from data.config import BOT_TIMEZONE


######################################## ПРОЧЕЕ ########################################
# Получение даты
def get_date(full: bool = True) -> str:
    if full:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
    else:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
