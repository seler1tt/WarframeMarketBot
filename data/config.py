# - *- coding: utf- 8 - *-
import configparser
import os

current_dir = os.getcwd()
path_data = current_dir + "\\data"
if os.path.exists(path_data):
    print("Data was found")
else:
    os.mkdir(path_data)

read_config = configparser.ConfigParser()
read_config.read('settings.ini')

BOT_VERSION = '1.0'
BOT_TOKEN = read_config['settings']['token'].strip()  # Токен бота
PATH_LOGS = 'data/logs.log'  # Путь к Логам
PATH_DATABASE = 'data/database.db'  # Путь к БД
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота


# Получение администраторов бота
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read('settings.ini')

    admins = read_admins['settings']['admin_id'].strip()
    admins = admins.replace(' ', '')

    if ',' in admins:
        admins = admins.split(',')
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while '' in admins: admins.remove('')
    while ' ' in admins: admins.remove(' ')
    while '\r' in admins: admins.remove('\r')
    while '\n' in admins: admins.remove('\n')

    admins = list(map(int, admins))

    return admins

BOT_DESCRIPTION = f'<b>⚜ Bot Version: <code>{BOT_VERSION}</code>\n' \
                  f'♻ Bot created by @seler1tt</b>'
