from django.db.models import QuerySet
from users.models import User


class TgUser():

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.obj: QuerySet = User.objects.filter(chat_id=chat_id)

    def user_obj(self) -> int:
        """Получаем объект User из БД."""
        return self.obj[0] if self.obj else None
