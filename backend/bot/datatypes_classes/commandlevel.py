"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from classes import Bot

from .datatypesclass import Observer, Subject


class CommandStart(Observer):
    """Команда start."""
    def update(
            self, subject: Subject, bot: Bot, chat_id: int
    ) -> None:
        if subject._state == 'start':
            answer = {
                'chat_id': chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)
