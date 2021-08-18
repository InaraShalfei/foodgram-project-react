import djoser.views
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from api.models import UserFollow
from users.models import User
from api.serializers import UserFollowedSerializer
from users.serializers import CustomUserSerializer


class UserViewSet(djoser.views.UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'delete'], url_path='subscribe',
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        followed = get_object_or_404(User, pk=pk)
        follower = request.user
        if request.method == 'GET':
            UserFollow.objects.get_or_create(follower=follower,
                                             followed=followed)
            serializer = UserFollowedSerializer(
                context=self.get_serializer_context()
            )
            return Response(serializer.to_representation(instance=followed),
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            UserFollow.objects.filter(follower=follower,
                                      followed=followed).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='subscriptions',
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        authors_queryset = User.objects.filter(
            user_followed__follower=request.user
        )
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        authors = paginator.paginate_queryset(authors_queryset,
                                              request=request)
        serializer = ListSerializer(child=UserFollowedSerializer(),
                                    context=self.get_serializer_context())
        return paginator.get_paginated_response(
            serializer.to_representation(authors)
        )
