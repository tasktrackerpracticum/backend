"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from django.contrib.auth.tokens import default_token_generator

import requests
from bot.config import config
from bot.classes.bot import Bot
from bot.classes.tguser import TgUser
from bot.keyboards.inline import to_tasktracker_kbrd
from bot.utils import texts as t
from djoser.utils import encode_uid

from .datatypesclass import Observer, Subject


class CommandStart(Observer):
    """Команда start."""
    def update(
            self, subject: Subject, tgbot: Bot, tguser: TgUser
    ) -> None:
        if subject._state == 'start':
            answer = {'chat_id': tguser.chat_id, 'text': t.UNKNOWN}
            if tguser.user_obj():
                answer['text'] = t.START_TEXT
            tgbot.send_answer(answer)


class CommandSetPassword(Observer):
    """Команда setpassword."""
    def update(
            self, subject: Subject, tgbot: Bot, tguser: TgUser
    ) -> None:
        if 'setpassword' in subject._state:
            if user := tguser.user_obj():
                answer = {'chat_id': tguser.chat_id}
                data = {
                    "uid": encode_uid(user.id),
                    "token": default_token_generator.make_token(user),
                    "new_password": subject._state.split(' ')[1]
                }
                url = config.PASSWORD_RESET_CONFIRM_URL
                response = requests.post(url, data)
                if response.status_code in {201, 204}:
                    answer['text'] = t.SET_PASSWORD_DONE
                    answer['reply_markup'] = to_tasktracker_kbrd()
                else:
                    answer['text'] = t.SET_PASSWORD_ERROR
                tgbot.send_answer(answer)
