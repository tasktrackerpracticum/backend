from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES
from timezone_utils.fields import TimeZoneField

from .managers import MyUserManager


class User(AbstractUser):

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
        null=True,
        blank=True,
    )
    chat_id = models.BigIntegerField(
        'Telegram user id',
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='media/users',
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
        null=True,
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
        null=True,
        blank=True,
    )
    country = models.CharField(
        'Страна',
        max_length=20,
        null=True,
        blank=True,
    )
    timezone = TimeZoneField(
        'Часовой пояс',
        choices=PRETTY_ALL_TIMEZONES_CHOICES,
        null=True,
        blank=True,
    )
    password = models.CharField('Пароль', max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return f"{self.email}({self.pk})"
