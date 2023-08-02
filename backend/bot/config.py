import os

from django.conf import settings

load_dotenv()


class Conf():
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    BASE_URL: str = 'https://taksa-tracker.ru/'
    WEBHOOK_URL: str = f'{BASE_URL}webhook/'
    TELEGRAM_URL: str = f'https://api.telegram.org/bot{BOT_TOKEN}/'
    PASSWORD_RESET_CONFIRM_URL: str = (
        f'{BASE_URL}api/v1/users/reset_password_confirm/'
    )
    TEMPLATES_DIR: str = settings.BASE_DIR / 'bot/templates/'
    COMMANDS: list[dict[str, str]] = [
        {
            'command': 'setpassword',
            'description': 'Сменить пароль к TaskTracker'
        },
    ]


config = Conf()
