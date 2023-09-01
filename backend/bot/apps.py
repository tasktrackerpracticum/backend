from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from bot.classes.bot import tg_bot
        from bot.config import config
        tg_bot.set_webhook({'url': config.WEBHOOK_URL})
        tg_bot.set_commands()
