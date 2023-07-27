import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bot.classes.bot import Bot
from bot.datatypes_classes import Road

from .datatypes_classes import HighLevelCommand


@csrf_exempt
def webhook(request):
    # Получаем словарь из тела полученного вебхука
    try:
        from_tg = json.loads(request.body)
    except Exception:
        from_tg = {}
    # Создаём объект Bot для работы с данными с вебхука
    bot = Bot()
    # Получаем chat_id пользователя
    chat_id = bot.chat_id(from_tg)
    # Получаем объект message
    message = bot.get_message(from_tg)
    # Получаем тип обновления
    if data_type := bot.get_data_type(from_tg):
        # Создаём объект Road, определяющий направление движения
        road = Road()
        # Набор возможных направлений движения
        pathes = (HighLevelCommand(),)
        # Добавляем направления к нашему объекту Road
        for path in pathes:
            road.attach(path)
        # Запускаем движения по выбранному направлению,
        # определяемому параметром data_type
        road.go(data_type, bot, chat_id, message=message)
    return HttpResponse('Hello', status=200)
