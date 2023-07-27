import json

from django.conf import settings


def set_password_kbrd(uid: str, token: int) -> str:
    """Кнопка Восстановления пароля."""
    inline_button = [{
        'text': 'Создать пароль',
        'url': (
            f'{settings.BASE_URL}{settings.PASSWORD_RESET_CONFIRM_URL}'
            f'/{uid}/{token}/'
        )
    }]
    return json.dumps({'inline_keyboard': [inline_button]})
