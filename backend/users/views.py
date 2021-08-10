from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserFollowSerializer
from users.models import User
from users.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'delete'], url_path='subscribe',
            permission_classes=permissions.IsAuthenticated)
    def subscribe(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = UserFollowSerializer()
            return Response(serializer.to_representation(instance=user), status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            # User.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


