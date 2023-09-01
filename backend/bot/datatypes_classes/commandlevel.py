"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""
import requests
from djoser.utils import encode_uid

from django.contrib.auth.tokens import default_token_generator

from bot.classes.bot import Bot
from bot.classes.tguser import TgUser
from bot.config import config
from bot.keyboards.inline import to_tasktracker_kbrd
from bot.utils import texts

from .datatypesclass import Observer, Subject


class CommandStart(Observer):
    """Команда start."""

    def update(
            self, subject: Subject, tgbot: Bot, tg_user: TgUser
    ) -> None:
        if subject.state == 'start':
            answer = {
                'chat_id': tg_user.chat_id,
                'text': (
                    texts.START_TEXT if tg_user.user_obj()
                    else texts.UNKNOWN
                )
            }
            tgbot.send_answer(answer)


class CommandSetPassword(Observer):
    """Команда setpassword."""
    def update(
            self, subject: Subject, tgbot: Bot, tguser: TgUser
    ) -> None:
        if 'setpassword' in subject.state:
            if user := tguser.user_obj():
                answer = {'chat_id': tguser.chat_id}
                data = {
                    "uid": encode_uid(user.id),
                    "token": default_token_generator.make_token(user),
                    "new_password": subject.state.split(' ')[1]
                }
                url = config.PASSWORD_RESET_CONFIRM_URL
                response = requests.post(url, data)
                if response.status_code in {201, 204}:
                    answer['text'] = texts.SET_PASSWORD_DONE
                    answer['reply_markup'] = to_tasktracker_kbrd()
                else:
                    answer['text'] = texts.SET_PASSWORD_ERROR
                tgbot.send_answer(answer)
