# - *- coding: utf- 8 - *-
from html import escape

from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from keyboards.inline_all import items_choice, orders_switch
from loader import dp
from utils.misc.bot_logging import bot_logger
from utils.warframe_market import find_items, get_item, get_orders

ORDER_TYPES = {
    "sell": {"title": "🛒 Продают (сначала дешёвые)", "action": "buy", "empty": "продавцов"},
    "buy": {"title": "💰 Покупают (сначала дорогие)", "action": "sell", "empty": "покупателей"},
}


@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: Message):
    await message.answer(
        "<b>🔎 Поиск на warframe.market</b>\n\n"
        "Напишите название предмета, например: <code>Khora Prime Blueprint</code>\n"
        "Можно и по-русски: <code>Кора Прайм Чертеж</code>\n\n"
        "Бот покажет 5 лучших предложений от игроков, которые сейчас в игре: "
        "кто продаёт дешевле всех или кто покупает дороже всех. "
        "Переключаться можно кнопками под сообщением.\n"
        "К каждому предложению есть готовое сообщение для личной переписки "
        "(нажмите, чтобы скопировать)."
    )


# Текст с заказами по предмету
async def orders_text(item, order_type):
    info = ORDER_TYPES[order_type]
    orders = await get_orders(item['slug'], order_type)

    text = f"<b>{escape(item['name'])}</b>\n" \
           f"https://warframe.market/items/{item['slug']}\n\n" \
           f"<b>{info['title']}</b>\n"

    if not orders:
        return text + f"\nСейчас нет {info['empty']} в игре."

    for order in orders:
        name = order['user']['ingameName']
        item_name = item['name']
        if 'rank' in order:
            item_name += f" (rank {order['rank']})"

        whisper = f'/w {name} Hi! I want to {info["action"]}: "{item_name}" ' \
                  f'for {order["platinum"]} platinum. (warframe.market)'

        text += f"\n💎 <b>{order['platinum']}</b> пл. · {escape(name)} · " \
                f"шт: {order['quantity']} · репутация: {order['user']['reputation']}\n" \
                f"<code>{escape(whisper)}</code>\n"

    return text


@dp.message_handler(content_types=['text'], state="*")
async def search_item(message: Message):
    try:
        items = await find_items(message.text)
    except Exception:
        bot_logger.exception("warframe.market items request failed")
        return await message.answer("❗ warframe.market не отвечает, попробуйте позже.")

    if not items:
        await message.answer("Ничего не найдено. Проверьте название предмета.")
    elif len(items) == 1:
        await send_orders(message, items[0], "sell")
    else:
        text = f"Найдено предметов: {len(items)}. Выберите нужный:"
        if len(items) > 10:
            text += "\n<i>Показаны первые 10, уточните запрос, если нужного нет.</i>"

        await message.answer(
            text,
            reply_markup=items_choice(items),
        )


# Выбор предмета из списка найденных
@dp.callback_query_handler(text_startswith="item:", state="*")
async def choice_item(call: CallbackQuery):
    await show_orders(call, call.data.split(":")[1], "sell")


# Переключение продают/покупают
@dp.callback_query_handler(text_startswith="orders:", state="*")
async def switch_orders(call: CallbackQuery):
    order_type, slug = call.data.split(":")[1:]
    await show_orders(call, slug, order_type)


async def show_orders(call: CallbackQuery, slug, order_type):
    item = await get_item(slug)
    await call.answer()

    if item is None:
        return await call.message.edit_text("Предмет не найден.")

    await send_orders(call.message, item, order_type, edit=True)


async def send_orders(message: Message, item, order_type, edit=False):
    try:
        text = await orders_text(item, order_type)
    except Exception:
        bot_logger.exception("warframe.market orders request failed")
        text = "❗ warframe.market не отвечает, попробуйте позже."

    keyboard = orders_switch(item['slug'], order_type)

    if edit:
        try:
            await message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)
