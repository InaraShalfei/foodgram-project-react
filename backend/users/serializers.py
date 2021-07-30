from djoser.serializers import UserCreateSerializer


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
