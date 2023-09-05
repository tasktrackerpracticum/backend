"""
Класс направлений верхнего уровня.

Идет перенаправление в зависимости от получения одного из 4 состояний:
- Состояние юзера;
- Команда;
- Callback_query;
- Текст.
"""

from bot.classes.bot import Bot
from bot.classes.tguser import TgUser

from .datatypesclass import Observer, Road, Subject


class HighLevelCommand(Observer):
    """Command update handler."""

    def update(
            self, subject: Subject, tg_bot: Bot, tg_user: TgUser, **kwargs,
    ) -> None:
        """Направления при получении комманды."""
        from .commandlevel import CommandSetPassword, CommandStart
        if subject.state == 'command':
            command = kwargs['message']['text'][1:]
            road = Road()
            paths = (CommandStart(), CommandSetPassword())
            for path in paths:
                road.attach(path)
            road.go(command, tg_bot, tg_user)
