# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb


# Выбор предмета, если по запросу нашлось несколько
def items_choice(items, limit=10):
    keyboard = InlineKeyboardMarkup()

    for item in items[:limit]:
        keyboard.add(
            ikb(item['name'], callback_data=f"item:{item['slug']}")
        )
    return keyboard


# Переключение между продавцами и покупателями (повторное нажатие - обновить)
def orders_switch(slug, order_type):
    keyboard = InlineKeyboardMarkup()

    sell_text = "🛒 Продают"
    buy_text = "💰 Покупают"
    if order_type == "sell":
        sell_text = f"🔄 {sell_text}"
    else:
        buy_text = f"🔄 {buy_text}"

    keyboard.add(
        ikb(sell_text, callback_data=f"orders:sell:{slug}"),
        ikb(buy_text, callback_data=f"orders:buy:{slug}"),
    )
    return keyboard
