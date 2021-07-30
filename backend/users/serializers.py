from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name', 'id', 'is_subscribed')
        model = CustomUser

