import json

from django.conf import settings


def to_tasktracker_kbrd() -> str:
    """Кнопка Перейти в TaskTracker."""
    inline_button = [{
        'text': 'Перейти в TaskTracker',
        'url': settings.BASE_URL
    }]
    return json.dumps({'inline_keyboard': [inline_button]})
