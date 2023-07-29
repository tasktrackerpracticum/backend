"""
    Класс направлений верхнего уровня.
    Идет перенаправление в зависимости от получения одного из 4 состояний:
    - Состояние юзера;
    - Команда;
    - Callback_query;
    - Текст.
"""

from bot.classes.tguser import TgUser
from bot.classes.bot import Bot

from .datatypesclass import Observer, Road, Subject


class HighLevelCommand(Observer):
    def update(
            self, subject: Subject, tgbot: Bot, tguser: TgUser, **kwargs
    ) -> None:
        """Направления при получении комманды."""
        from .commandlevel import CommandSetPassword, CommandStart
        if subject._state == 'command':
            command = kwargs['message']['text'][1:]
            road = Road()
            pathes = (CommandStart(), CommandSetPassword())
            for path in pathes:
                road.attach(path)
            road.go(command, tgbot, tguser)
