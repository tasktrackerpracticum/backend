import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot.classes.bot import bot
from bot.datatypes_classes import Road

from .datatypes_classes import HighLevelCommand


@csrf_exempt
def webhook(request):
    try:
        from_tg = json.loads(request.body)
    except Exception:
        return HttpResponse('Hello', status=200)
    chat_id = bot.chat_id(from_tg)
    message = bot.get_message(from_tg)
    if data_type := bot.get_data_type(from_tg):
        road = Road()
        pathes = (HighLevelCommand(),)
        for path in pathes:
            road.attach(path)
        road.go(data_type, bot, chat_id, message=message)
    return HttpResponse('Hello', status=200)
