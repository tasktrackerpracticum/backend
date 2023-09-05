from django.db import models

from users.models import User


class CreatedAtUpdatedAt(models.Model):
    """Abstract model mixin, add created_at, updated_at fields."""

    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    """Tag model."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tags')
    title = models.CharField('Название тега', max_length=100)
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='tags')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Redefine save method."""
        self.title = self.title.capitalize()
        super().save(*args, **kwargs)


class Project(CreatedAtUpdatedAt):
    """Project model."""

    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='ProjectUser')
    description = models.TextField('Описание проекта', blank=True, null=True)
    date_start = models.DateField('Дата начала', blank=True, null=True)
    date_finish = models.DateField('Дата завершения', blank=True, null=True)
    is_active = models.BooleanField('Статус', default=True, null=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title


class ProjectUser(models.Model):
    """ProjectUser model."""

    OBSERVER = 'observer'
    BASE_USER = 'user'
    PROJECT_MANAGER = 'pm'
    FORBIDDEN = 'forbidden'

    ROLES = (
        (OBSERVER, 'наблюдатель'),
        (BASE_USER, 'базовый пользователь'),
        (PROJECT_MANAGER, 'ПМ'),
        (FORBIDDEN, 'запрещено'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f'ProjectUser ({self.id})'


class Task(CreatedAtUpdatedAt):
    """Task model."""

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
    description = models.TextField(blank=True, null=True)
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
        return f'{self.project} ({self.title})'


class TaskFile(models.Model):
    """TaskFile model."""

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/tasks')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'File ({self.id})'


class TaskImage(models.Model):
    """Image model."""

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/tasks')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'Image ({self.id})'


class Comment(CreatedAtUpdatedAt):
    """Comment model."""

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment ({self.id})'
