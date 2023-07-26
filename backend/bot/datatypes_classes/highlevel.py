"""
    Класс направлений верхнего уровня.
    Идет перенаправление в зависимости от получения одного из 4 состояний:
    - Состояние юзера;
    - Команда;
    - Callback_query;
    - Текст.
"""

from classes import Bot
from .datatypesclass import Observer, Road, Subject


class HighLevelCommand(Observer):
    def update(
            self, subject: Subject, bot: Bot, chat_id: int, **kwargs
    ) -> None:
        """Направления при получении комманды."""
        from .commandlevel import CommandStart
        if subject._state == 'command':
            command = kwargs['message']['text'][1:]
            road = Road()
            pathes = (CommandStart(),)
            for path in pathes:
                road.attach(path)
            road.go(command, bot, chat_id)
