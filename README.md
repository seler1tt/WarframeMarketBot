# Warframe Market Bot

A Telegram bot for quick price checks on [warframe.market](https://warframe.market).
Send it an item name and it replies with the best offers from players who are **in game right now**,
together with a ready-to-copy whisper message for each one.

## Features

- **Item search by name**, in English or Russian: `Khora Prime Blueprint`, `Кора Прайм Чертеж`, or just `khora prime`.
  If several items match, the bot shows up to 10 of them as buttons to pick from.
- **Sellers and buyers.** Two buttons switch between:
  - 🛒 **Selling**: the 5 cheapest sellers;
  - 💰 **Buying**: the 5 buyers paying the most.

  Pressing the active button again refreshes the prices.
- **Ready-made whisper** for every offer, in the same format as the website.
  In Telegram it is shown as code, so a tap copies it:
  ```
  /w PlayerName Hi! I want to buy: "Khora Prime Blueprint" for 25 platinum. (warframe.market)
  ```
  The rank is added for mods and arcanes, e.g. `"Arcane Energize (rank 5)"`.
- Only players with the `ingame` status are listed, since those are the ones you can trade with right away.
- **Admin tools:** a startup notification, a daily database backup and commands to download the database and logs.
- **Anti-flood:** non-admin users are limited to one message every 0.5 s.

## Requirements

- **Python 3.11**
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

> The bot is built on **aiogram 2.x**, which requires `aiohttp < 3.9`.
> Prebuilt wheels for that aiohttp version don't exist for Python 3.12+, and it fails to compile from source there,
> so stay on Python 3.11.

## Installation

```bash
git clone <repo-url>
cd WarframeMarketBot

# with uv
uv venv --python 3.11 .venv
uv pip install -r requirements.txt

# or with plain pip
py -3.11 -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

## Configuration

Copy `settings.example.ini` to `settings.ini` and fill it in:

```ini
[settings]
token=123456789:AAExampleTokenFromBotFather
admin_id=111111111, 222222222
```

| Key        | Description                                                                                          |
|------------|------------------------------------------------------------------------------------------------------|
| `token`    | Bot token from @BotFather                                                                            |
| `admin_id` | Telegram user IDs of the admins, comma-separated. You can find your ID with [@userinfobot](https://t.me/userinfobot) |

`settings.ini` is listed in `.gitignore`. Never commit your token.

## Running

Run the bot from the project root, because `settings.ini` and `data/` are resolved relative to the working directory:

```bash
.venv\Scripts\python main.py        # Windows
# .venv/bin/python main.py          # Linux / macOS
```

On first start the bot creates `data/database.db` (users) and `data/logs.log`.

## Commands

| Command              | Who     | Description                      |
|----------------------|---------|----------------------------------|
| `/start`, `/help`    | anyone  | Usage instructions               |
| *any text*           | anyone  | Search for an item by name       |
| `/db`, `/database`   | admins  | Download the database file       |
| `/log`, `/logs`      | admins  | Download the log file            |

The bot also sends admins a backup of the database every day at midnight (server time).

## Project structure

```
├── main.py                  # Entry point: startup, scheduler, polling
├── loader.py                # Bot, Dispatcher and scheduler instances
├── settings.example.ini     # Config template
├── requirements.txt
├── data/
│   └── config.py            # Reads settings.ini, paths, timezone
├── handler/
│   ├── main_handler.py      # /start, item search, sellers/buyers switching
│   └── admin/admin_menu.py  # /db and /log admin commands
├── keyboards/
│   └── inline_all.py        # Item choice and sell/buy buttons
├── middlewares/
│   ├── exists_user.py       # Saves new users to the database
│   └── throttling.py        # Anti-flood
├── services/
│   └── api_sqlite.py        # SQLite helpers
└── utils/
    ├── warframe_market.py   # warframe.market API v2 client
    ├── misc_functions.py    # Admin notifications and auto-backup
    ├── const_functions.py   # Date helpers
    └── misc/                # Filters and logging setup
```

## How it works

The bot uses the public [warframe.market API v2](https://api.warframe.market/v2) for the PC platform:

- `GET /v2/items` returns the full item list (about 3,900 items) with English and Russian names.
  It is cached in memory for 12 hours.
- `GET /v2/orders/item/{slug}` returns all orders for an item. The bot keeps orders from `ingame` users and sorts sell orders
  by price ascending and buy orders by price descending.
