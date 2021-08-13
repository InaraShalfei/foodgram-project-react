from rest_framework import serializers
from rest_framework.serializers import Serializer

from api.models import UserFollow


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        return UserFollow.objects.filter(followed=obj,
                                         follower=self.context.get('request').user).exists()
