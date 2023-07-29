from celery import shared_task
from datetime import datetime, timedelta
from tasks.models import Task
from bot.classes.notifications import notification


@shared_task
def deadline_task() -> None:
    """Рассылка оповещений о завтрашнем дедлайне задач."""
    tasks = (
        Task.objects.filter(deadline__lte=datetime.now() + timedelta(days=1))
        .exclude(deadline__isnull=False)
    )
    for task in tasks:
        users = task.users.all()
        for user in users:
            notification.send(type='deadline', task=task, user=user)
