from django.contrib.auth.models import AbstractUser as DjangoUser
from django.db import models


class User(DjangoUser):
    email = models.EmailField(blank=False, unique=True,
                              verbose_name='user email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
