"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

import requests
from backend.bot.classes.bot import Bot
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import encode_uid
from bot.utils import texts as t

from bot.classes.tguser import TgUser
from bot.keyboards.inline import to_tasktracker_kbrd

from .datatypesclass import Observer, Subject


class CommandStart(Observer):
    """Команда start."""
    def update(
            self, subject: Subject, bot: Bot, chat_id: int
    ) -> None:
        if subject._state == 'start':
            tguser = TgUser(chat_id)
            answer = {'chat_id': chat_id, 'text': t.UNKNOWN}
            if tguser.user_obj():
                answer['text'] = t.START_TEXT
            bot.send_answer(answer)


class CommandSetPassword(Observer):
    """Команда setpassword."""
    def update(
            self, subject: Subject, bot: Bot, chat_id: int
    ) -> None:
        if 'setpassword' in subject._state:
            tguser = TgUser(chat_id)
            if user := tguser.user_obj():
                answer = {'chat_id': chat_id}
                data = {
                    "uid": encode_uid(user.id),
                    "token": default_token_generator.make_token(user),
                    "new_password": subject._state.split(' ')[1]
                }
                url = (
                    f'{settings.BASE_URL}{settings.PASSWORD_RESET_CONFIRM_URL}'
                )
                response = requests.post(url, data)
                if response.status_code == 201:
                    answer['text'] = t.SET_PASSWORD_DONE
                    answer['reply_markup'] = to_tasktracker_kbrd
                else:
                    answer['text'] = t.SET_PASSWORD_ERROR
            bot.send_answer(answer)
