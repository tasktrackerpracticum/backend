from django.apps import AppConfig
from django.conf import settings


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from bot.classes import Bot
        bot = Bot(settings.BOT_TOKEN)
        url = f'/webhook/{settings.BOT_TOKEN}/'
        data = {
            'url': f'{settings.BASE_URL}{url}'
        }
        bot.set_webhook(data)