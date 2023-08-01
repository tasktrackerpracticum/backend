from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from bot.classes.bot import tgbot
        from bot.config import config
        tgbot.set_webhook({'url': config.WEBHOOK_URL})
        tgbot.set_commands()
