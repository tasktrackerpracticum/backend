from users.models import User


class TgUser():

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.obj = User.objects.filter(chat_id=self.chat_id)

    def user_obj(self) -> int:
        return self.obj[0] if self.obj else None
