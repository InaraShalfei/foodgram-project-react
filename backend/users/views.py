from rest_framework import viewsets, permissions, mixins

from .models import CustomUser
from .paginatiors import StandardPagination
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id', ).all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticated]
