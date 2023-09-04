import json
from typing import Any

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from bot.classes.bot import tg_bot
from bot.classes.tguser import TgUser
from bot.datatypes_classes import Road

from .datatypes_classes import HighLevelCommand


@csrf_exempt
def webhook(request):
    """Set webhook for telegram bot."""
    try:
        from_tg: dict[str, Any] = json.loads(request.body)
    except Exception:
        return HttpResponse('Hello', status=status.HTTP_400_BAD_REQUEST)
    message = tg_bot.get_message(from_tg)
    if data_type := tg_bot.get_data_type(from_tg):
        road = Road()
        paths = (HighLevelCommand(),)
        tg_user = TgUser(tg_bot.chat_id(from_tg))
        for path in paths:
            road.attach(path)
        road.go(data_type, tg_bot, tg_user, message=message)
    return HttpResponse('Hello', status=status.HTTP_200_OK)
