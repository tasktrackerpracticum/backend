import os

from django.conf import settings


class Conf():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BASE_URL = 'https://taksa-tracker.ru/'
    WEBHOOK_URL = f'webhook/{BOT_TOKEN}/'
    PASSWORD_RESET_CONFIRM_URL = 'users/reset_password_confirm/'
    TEMPLATES_DIR = settings.BASE_DIR / 'bot/temlates/'
    COMMANDS = [
        {
            'command': 'setpassword',
            'description': 'Сменить пароль к TaskTracker'
        },
    ]


config = Conf()
