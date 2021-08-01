from rest_framework import mixins, viewsets

from api.models import Tag
from api.paginators import TagsPagination
from api.serializers import TagSerializer


class ViewSet(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    pass


class TagViewSet(ViewSet):
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagsPagination



