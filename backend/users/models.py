from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES
from timezone_utils.fields import TimeZoneField

from .managers import MyUserManager


class User(AbstractUser):
    """User class for project."""

    MALE = 'male'
    FEMALE = 'female'

    GENDERS = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(
        'Имя пользователя',
        max_length=100,
        blank=True,
    )
    chat_id = models.BigIntegerField(
        'Telegram user id',
        null=True,
        blank=True,
    )
    notify_in_chat = models.BooleanField(
        'Уведомлять в телеграмм',
        default=False,
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='users',
        null=True, blank=True,
    )
    phone = PhoneNumberField(
        region='RU',
        verbose_name='Телефон',
        blank=True,
        null=True,
    )
    position = models.CharField(
        'Должность',
        max_length=100,
        blank=True,
    )
    date_of_birth = models.DateField(
        'Дата рождения',
        null=True,
        blank=True,
    )
    gender = models.CharField(
        'Пол',
        max_length=6,
        choices=GENDERS,
        blank=True,
    )
    country = models.CharField(
        'Страна',
        max_length=20,
        blank=True,
    )
    timezone = TimeZoneField(
        'Часовой пояс',
        choices=PRETTY_ALL_TIMEZONES_CHOICES,
        null=True,
        blank=True,
    )
    password = models.CharField('Пароль', max_length=200)
    last_login = models.DateTimeField(verbose_name='Время последней активности')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}({self.pk})'

    @property
    def is_admin(self):
        """Check user is superuser or user is staff."""
        return self.is_superuser or self.is_staff
