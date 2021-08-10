from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import UserFollow
from api.serializers import UserFollowSerializer
from users.models import User
from users.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'delete'], url_path='subscribe',
            permission_classes=permissions.IsAuthenticated)
    def subscribe(self, request, pk):
        followed = User.objects.get(pk=pk)
        follower = request.user
        if request.method == 'GET':
            UserFollow.objects.get_or_create(follower=follower, followed=followed)
            serializer = UserFollowSerializer()
            return Response(serializer.to_representation(instance=followed), status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            UserFollow.objects.filter(follower=follower, followed=followed).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



