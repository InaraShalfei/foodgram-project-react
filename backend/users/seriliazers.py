from djoser.conf import settings
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        return True

