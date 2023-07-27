"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from backend.bot.classes.bot import Bot
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import encode_uid

from bot.classes.tguser import TgUser
from bot.keyboards.inline import set_password_kbrd

from .datatypesclass import Observer, Subject


class CommandStart(Observer):
    """Команда start."""
    def update(
            self, subject: Subject, bot: Bot, chat_id: int
    ) -> None:
        if subject._state == 'start':
            tguser = TgUser(chat_id)
            answer = {'chat_id': chat_id, 'text': 'Вы кто такой?'}
            if user := tguser.user_obj():
                uid = encode_uid(user.id)
                token = default_token_generator.make_token(user)
                keyboard = set_password_kbrd(uid, token)
                answer['text'] = 'Чтобы установить пароль, нажми на кнопку:'
                answer['reply_markup'] = keyboard
            bot.send_answer(answer)
