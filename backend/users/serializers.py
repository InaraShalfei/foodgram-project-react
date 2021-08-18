from djoser.conf import settings
from djoser.serializers import UserSerializer

from users.mixins import IsSubscribedMixin
from users.models import User


class CustomUserSerializer(UserSerializer, IsSubscribedMixin):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)
