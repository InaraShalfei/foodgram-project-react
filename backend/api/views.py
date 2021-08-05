from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api.models import Tag, Ingredient, Recipe
from api.serializers import (
    TagSerializer, IngredientSerializer,
    RecipeWriteSerializer, RecipeReadSerializer
)


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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    # TODO copy author assignment from api_yamdb reviews.views.ReviewViewSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RecipeReadSerializer
        return RecipeWriteSerializer

