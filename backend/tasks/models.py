from django.db import models

from users.models import User


class Organization(models.Model):
    title = models.CharField(max_length=200, unique=True)
    users = models.ManyToManyField(User, through='OrganizationUser')

    def __str__(self):
        return self.title


class OrganizationUser(models.Model):

    OBSERVER = 'наблюдатель'
    BASE_USER = 'базовый пользователь'
    PROJECT_MANAGER = 'ПМ'
    CREATOR = 'создатель'
    FORBIDDEN = 'запрещено'

    ROLES = (
        (OBSERVER, 'наблюдатель'),
        (BASE_USER, 'базовый пользователь'),
        (PROJECT_MANAGER, 'ПМ'),
        (CREATOR, 'создатель'),
        (FORBIDDEN, 'запрещено')
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='organization_users'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_organizations'
    )
    role = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        unique_together = ('organization', 'user',)

    def __str__(self):
        return f"{self.organization}: {self.user} -> {self.role}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    users = models.ManyToManyField(User, through='ProjectUser')


class ProjectUser(models.Model):

    OBSERVER = 'наблюдатель'
    BASE_USER = 'базовый пользователь'
    PROJECT_MANAGER = 'ПМ'
    FORBIDDEN = 'запрещено'

    ROLES = (
        (OBSERVER, 'наблюдатель'),
        (BASE_USER, 'базовый пользователь'),
        (PROJECT_MANAGER, 'ПМ'),
        (FORBIDDEN, 'запрещено')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)


class Task(models.Model):

    BACKLOG = 'Беклог'
    TODO = 'В работе'
    TEST = 'Тестирование'
    DONE = 'Завершено'
    DELETED = 'Удалено'

    COLUMNS = (
        (BACKLOG, 'Беклог'),
        (TODO, 'В работе'),
        (TEST, 'Тестирование'),
        (DONE, 'Завершено'),
        (DELETED, 'Удалено'),
    )

    URGENTLY = 'Срочно'
    NONURGENTLY = 'Несрочно'

    STATUSES = (
        (URGENTLY, 'Срочно'),
        (NONURGENTLY, 'Несрочно'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    column = models.CharField(max_length=15, choices=COLUMNS)
    users = models.ManyToManyField(User, related_name='tasks')
    project = models.ForeignKey(
        Project, related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='tasks_author', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUSES)
    deadline = models.DateTimeField()


# class TaskUser(models.Model):
#     task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)


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


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    image = models.ImageField(upload_to='media/comments')
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)


class Subtask(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='task')
    subtask = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='subtask')
