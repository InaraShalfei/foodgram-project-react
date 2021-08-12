import djoser.views

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from api.models import UserFollow
from api.serializers import UserFollowedSerializer
from users.models import User
from users.serializers import CustomUserSerializer


class UserViewSet(djoser.views.UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'delete'], url_path='subscribe',
            permission_classes=permissions.IsAuthenticated)
    def subscribe(self, request, pk):
        followed = User.objects.get(pk=pk)
        follower = request.user
        if request.method == 'GET':
            UserFollow.objects.get_or_create(follower=follower, followed=followed)
            serializer = UserFollowedSerializer(context=self.get_serializer_context())
            return Response(serializer.to_representation(instance=followed), status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            UserFollow.objects.filter(follower=follower, followed=followed).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='subscriptions',
            permission_classes=permissions.IsAuthenticated)
    def subscriptions(self, request):
        subscriptions = UserFollow.objects.filter(follower=request.user).all()
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        subscriptions_page = paginator.paginate_queryset(subscriptions, request=request)
        followed_list = [subscription.followed for subscription in subscriptions_page]
        serializer = ListSerializer(child=UserFollowedSerializer(), context=self.get_serializer_context())
        return paginator.get_paginated_response(serializer.to_representation(followed_list))
