from datetime import datetime, timedelta

from celery import shared_task

from bot.classes.notifications import notification
from tasks.models import Task


@shared_task
def deadline_task() -> None:
    """Рассылка оповещений о завтрашнем дедлайне задач."""
    tasks = (
        Task.objects.filter(deadline__lte=datetime.now() + timedelta(days=1))
        .exclude(deadline__lte=datetime.now() + timedelta(hours=23))
    )
    for task in tasks:
        users = task.users.all()
        for user in users:
            if user.notify_in_chat:
                notification.send(type='deadline', task=task, user=user)
