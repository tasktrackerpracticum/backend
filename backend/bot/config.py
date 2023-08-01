import os

from dotenv import load_dotenv
from django.conf import settings

load_dotenv()


class Conf():
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    WEBHOOK_URL: str = 'https://taksa-tracker.ru/webhook/'
    TELEGRAM_URL: str = f'https://api.telegram.org/bot{BOT_TOKEN}/'
    PASSWORD_RESET_CONFIRM_URL: str = 'users/reset_password_confirm/'
    TEMPLATES_DIR: str = settings.BASE_DIR / 'bot/temlates/'
    COMMANDS: list[dict[str, str]] = [
        {
            'command': 'setpassword',
            'description': 'Сменить пароль к TaskTracker'
        },
    ]


config = Conf()
