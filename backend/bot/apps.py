from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from bot.classes.bot import bot
        from bot.config import config
        bot.set_webhook({'url': config.WEBHOOK_URL})
        bot.set_commands()
