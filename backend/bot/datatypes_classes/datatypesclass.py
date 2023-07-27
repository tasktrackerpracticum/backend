"""
    Классы, определяющие Наблюдателя и Подписчика,
    а также интерфейс для их взаимодействия.
"""

from abc import ABC, abstractmethod

from bot.classes.bot import Bot


class Subject(ABC):
    """ Интферфейс издателя объявляет набор методов
    для управлениями подписчиками."""

    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        """Присоединяет наблюдателя к издателю."""
        pass

    @abstractmethod
    def clean(self, observer: 'Observer') -> None:
        """Очищает список наблюдателей издателя."""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Уведомляет всех наблюдателей о событии."""
        pass


class Observer(ABC):
    """Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков."""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Получить обновление от субъекта."""
        pass


class Road(Subject):
    """Издатель владеет некоторым важным состоянием и оповещает наблюдателей
    о его изменениях."""

    _state: int = None
    """Для удобства в этой переменной хранится состояние Издателя, необходимое
    всем подписчикам."""

    _observers: list[Observer] = []
    """Список подписчиков."""

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def clean(self, observer: Observer) -> None:
        self._observers.clear()

    def notify(self, bot: Bot, chat_id: int, **kwargs) -> None:
        """Запуск обновления в каждом подписчике."""
        for observer in self._observers:
            observer.update(self, bot, chat_id, **kwargs)

        self.clean(observer)

    def go(self, state: str, bot: Bot, chat_id: int, **kwargs) -> None:
        """Получаем состояние state и запускаем оповещение всех
        прикреплённых на данный момент подписчиков."""
        self._state = state
        self.notify(bot, chat_id, **kwargs)
