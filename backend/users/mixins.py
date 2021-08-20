from rest_framework import serializers
from rest_framework.serializers import Serializer

from api.models import UserFollow


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return UserFollow.objects.filter(followed=obj, follower=user).exists()
