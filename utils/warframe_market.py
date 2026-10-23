# - *- coding: utf- 8 - *-
import time

import aiohttp

API_URL = "https://api.warframe.market/v2"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Language': 'ru',
    'Platform': 'pc',
}
ITEMS_CACHE_TTL = 12 * 60 * 60  # Как часто обновлять список предметов (сек)

_items_cache = {"items": [], "updated": 0}


async def _api_get(path):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(f"{API_URL}{path}") as resp:
            if resp.status == 404:
                return None
            resp.raise_for_status()
            return (await resp.json())['data']


# Получение всех предметов (с кэшем, список большой)
async def get_items():
    if not _items_cache["items"] or time.time() - _items_cache["updated"] > ITEMS_CACHE_TTL:
        items = []
        for item in await _api_get("/items"):
            names = [lang['name'] for lang in item['i18n'].values()]
            items.append({
                "slug": item['slug'],
                "name": item['i18n']['en']['name'],
                "search": [name.lower() for name in names],
            })

        _items_cache["items"] = items
        _items_cache["updated"] = time.time()

    return _items_cache["items"]


# Поиск предметов по названию (английскому или русскому)
async def find_items(query):
    query = " ".join(query.lower().split())
    items = await get_items()

    exact = [item for item in items if query in item['search']]
    if exact:
        return exact

    words = query.split()
    found = [
        item for item in items
        if any(all(word in name for word in words) for name in item['search'])
    ]
    return sorted(found, key=lambda item: len(item['name']))


async def get_item(slug):
    for item in await get_items():
        if item['slug'] == slug:
            return item


# Лучшие заказы от игроков, которые сейчас в игре:
# sell - самые дешёвые продавцы, buy - покупатели, которые платят больше всех
async def get_orders(slug, order_type, limit=5):
    orders = await _api_get(f"/orders/item/{slug}")
    if not orders:
        return []

    orders = [
        order for order in orders
        if order['type'] == order_type and order['user']['status'] == 'ingame'
    ]
    return sorted(orders, key=lambda order: order['platinum'], reverse=order_type == 'buy')[:limit]
