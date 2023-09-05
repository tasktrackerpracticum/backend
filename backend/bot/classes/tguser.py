from django.db.models import QuerySet

from users.models import User


class TgUser:
    """Telegram User Class."""

    def __init__(self, chat_id: int):
        """Initialise class."""
        self.chat_id = chat_id
        self.user: QuerySet = User.objects.filter(chat_id=chat_id)

    def user_obj(self) -> int:
        """Получаем объект User из БД."""
        return self.user.first()
