"""Команды бота."""
import contextlib
import json
from typing import Any

import requests
from bot.config import config


class Bot():

    def __init__(self):
        self.url = config.TELEGRAM_URL
        self.commands = config.COMMANDS

    def chat_id(self, data: dict[str, Any]) -> int:
        """Получение chat id пользователя в Telegram."""
        message_object = self.get_message(data)
        if 'chat' in message_object:
            return message_object['chat'].get('id', 0)
        if 'from' in message_object:
            return message_object['from'].get('id', 0)
        return 0

    @staticmethod
    def get_message(data: dict[str, Any]) -> dict[str, Any] | None:
        """Получение объекта message."""
        if 'message' in data:
            return data['message']
        if 'callback_query' in data:
            return data['callback_query'].get('message', {})
        return {}

    def send_answer(self, answer: dict[str, Any]) -> None:
        """Отправка сообщения в бот."""
        method = f'{self.url}sendMessage'
        with contextlib.suppress(Exception):
            requests.post(method, data=answer)

    def delete_webhook(self) -> None:
        """Удаление вебхука бота."""
        method = f'{self.url}deleteWebhook'
        with contextlib.suppress(Exception):
            requests.post(method)

    def set_webhook(self, data: dict[str, Any]) -> None:
        """Установка веб-хука бота."""
        method = f'{self.url}setWebhook'
        with contextlib.suppress(Exception):
            requests.post(method, data=data)

    def set_commands(self) -> None:
        """Установка комманд бота."""
        method = f'{self.url}setMyCommands'
        commands = json.dumps(self.commands)
        send_text = f'{method}?commands={commands}'
        with contextlib.suppress(Exception):
            requests.get(send_text)

    @staticmethod
    def get_content_type(message: dict[str, Any]) -> str:
        """Получение типа контента, поступвшего на вебхук."""
        contents = ['text', 'document', 'photo']
        return next(
            (content for content in contents if content in message), '')

    @staticmethod
    def get_data_type(data: dict[str, Any]) -> str | None:
        """Получение типа обновления, поступившего на вебхук."""
        if 'callback_query' in data:
            return 'callback_query'
        if 'message' in data and 'text' in data['message']:
            return (
                'command' if data['message']['text'].startswith('/')
                else 'text'
            )
        return ''


tgbot = Bot()
