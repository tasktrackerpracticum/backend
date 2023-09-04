"""Datatype class module.

Классы, определяющие Наблюдателя и Подписчика,
а также интерфейс для их взаимодействия.
"""

from abc import ABC, abstractmethod

from bot.classes.bot import Bot
from bot.classes.tguser import TgUser


class Subject(ABC):
    """Subject abstract class.

    Интерфейс издателя объявляет набор методов
    для управления подписчиками.
    """

    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        """Присоединяет наблюдателя к издателю."""

    @abstractmethod
    def clean(self, observer: 'Observer') -> None:
        """Очищает список наблюдателей издателя."""

    @abstractmethod
    def notify(self) -> None:
        """Уведомляет всех наблюдателей о событии."""


class Observer(ABC):
    """Observer abstract class.

    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Получить обновление от субъекта."""


class Road(Subject):
    """Road class.

    Издатель владеет некоторым важным состоянием и оповещает наблюдателей
    о его изменениях.
    """

    state: str | None = None
    """Для удобства в этой переменной хранится состояние Издателя, необходимое
    всем подписчикам."""

    _observers: list[Observer] = []
    """Список подписчиков."""

    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        self._observers.append(observer)

    def clean(self, observer: Observer) -> None:
        """Clean observer."""
        self._observers.clear()

    def notify(self, tgbot: Bot, tguser: TgUser, **kwargs) -> None:
        """Запуск обновления в каждом подписчике."""
        for observer in self._observers:
            observer.update(self, tgbot, tguser, **kwargs)

        self.clean(observer)

    def go(self, state: str, tgbot: Bot, tguser: TgUser, **kwargs) -> None:
        """Go method.

        Получаем состояние state и запускаем оповещение всех
        прикреплённых на данный момент подписчиков.
        """
        self.state = state
        self.notify(tgbot, tguser, **kwargs)
