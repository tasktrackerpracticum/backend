from django.contrib.auth.models import AbstractUser
from django.db import models
from timezone_utils.fields import TimeZoneField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES

from .managers import MyUserManager


class User(AbstractUser): # is_superuser, is_active, is_staff

    MALE = 'male'
    FEMALE = 'female'

    GENDERS = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    email = models.EmailField(unique=True)
    username = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='media/users', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDERS, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True) # Геоданные?
    timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES, null=True, blank=True)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return str(self.id)
