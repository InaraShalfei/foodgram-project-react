from rest_framework import filters, mixins, viewsets

from api.models import Tag, Ingredient
from api.serializers import TagSerializer, IngredientSerializer


class ViewSet(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    pass


class TagViewSet(ViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)

