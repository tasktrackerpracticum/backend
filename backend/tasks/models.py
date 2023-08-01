from django.db import models

from users.models import User


class CreatedAtUpdatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(CreatedAtUpdatedAt):
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='ProjectUser')
    description = models.TextField('Описание проекта', blank=True, null=True)
    date_start = models.DateField('Дата начала', blank=True, null=True)
    date_finish = models.DateField('Дата завершения', blank=True, null=True)
    is_active = models.BooleanField('Статус', default=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f"{self.title}"


class ProjectUser(models.Model):

    OBSERVER = 'observer'
    BASE_USER = 'user'
    PROJECT_MANAGER = 'pm'
    FORBIDDEN = 'forbidden'

    ROLES = (
        (OBSERVER, 'наблюдатель'),
        (BASE_USER, 'базовый пользователь'),
        (PROJECT_MANAGER, 'ПМ'),
        (FORBIDDEN, 'запрещено')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)


class Task(CreatedAtUpdatedAt):

    BACKLOG = 'backlog'
    TODO = 'todo'
    TEST = 'testing'
    DONE = 'done'
    DELETED = 'deleted'

    COLUMNS = (
        (BACKLOG, 'Беклог'),
        (TODO, 'В работе'),
        (TEST, 'Тестирование'),
        (DONE, 'Завершено'),
        (DELETED, 'Удалено'),
    )

    URGENTLY = 'urgent'
    NONURGENTLY = 'nonurgent'

    STATUSES = (
        (URGENTLY, 'Срочно'),
        (NONURGENTLY, 'Несрочно'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    column = models.CharField(max_length=15, choices=COLUMNS)
    users = models.ManyToManyField(User, related_name='tasks')
    project = models.ForeignKey(
        Project, related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='tasks_author', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUSES)
    deadline = models.DateTimeField(blank=True, null=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f"{self.project} ({self.title})"


class TaskFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to='media/tasks')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='files')


class TaskImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/tasks')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='images')


class Comment(CreatedAtUpdatedAt):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
