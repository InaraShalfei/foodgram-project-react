from django.contrib.auth.models import AbstractUser as DjangoUser


class User(DjangoUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
