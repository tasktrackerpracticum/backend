import json
from typing import Any

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.classes.tguser import TgUser

from bot.classes.bot import tgbot
from bot.datatypes_classes import Road

from .datatypes_classes import HighLevelCommand


@csrf_exempt
def webhook(request):
    try:
        from_tg: dict[str, Any] = json.loads(request.body)
    except Exception:
        return HttpResponse('Hello', status=200)
    message = tgbot.get_message(from_tg)
    if data_type := tgbot.get_data_type(from_tg):
        road = Road()
        pathes = (HighLevelCommand(),)
        tguser = TgUser(tgbot.chat_id(from_tg))
        for path in pathes:
            road.attach(path)
        road.go(data_type, tgbot, tguser, message=message)
    return HttpResponse('Hello', status=200)
