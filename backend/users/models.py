from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email', max_length=254)
    username = models.CharField(blank=True, max_length=150)
    first_name = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
