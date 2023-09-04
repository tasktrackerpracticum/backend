import json

from bot.config import config
from bot.utils import texts as t


def to_tasktracker_kbrd() -> str:
    """Кнопка Перейти в TaskTracker."""
    inline_button = [
        {
            'text': t.GOTO_TASKTRACKER,
            'url': config.BASE_URL,
        },
    ]
    return json.dumps({'inline_keyboard': [inline_button]})
