from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.mixins import ViewSet
from api.models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from api.permissions import CustomPermissions
from api.serializers import (
    FavoriteRecipeSerializer, IngredientSerializer,  RecipeReadSerializer,
    RecipeWriteSerializer, ShoppingCartSerializer, TagSerializer,
)


class TagViewSet(ViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    permission_classes = [CustomPermissions]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = bool(self.request.query_params.get('is_in_shopping_cart'))
        is_favorited = bool(self.request.query_params.get('is_favorited'))
        if is_in_shopping_cart:
            queryset = queryset.filter(shopping_carts__user=self.request.user)
        if is_favorited:
            queryset = queryset.filter(favorite_recipes__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context

    @action(detail=True, methods=['get', 'delete'], url_path='favorite',
            permission_classes=permissions.IsAuthenticatedOrReadOnly)
    def favorite(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        user = request.user
        if request.method == 'GET':
            favorite_recipe, created = FavoriteRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            serializer = FavoriteRecipeSerializer()
            return Response(serializer.to_representation
                            (instance=favorite_recipe),
                            status=status.HTTP_201_CREATED
                            )

        if request.method == 'DELETE':
            FavoriteRecipe.objects.filter(user=user,
                                          recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'], url_path='shopping_cart',
            permission_classes=permissions.IsAuthenticatedOrReadOnly)
    def shopping_cart(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        user = request.user
        if request.method == 'GET':
            recipe, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            serializer = ShoppingCartSerializer()
            return Response(serializer.to_representation(instance=recipe),
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            ShoppingCart.objects.filter(user=user,
                                        recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            permission_classes=permissions.IsAuthenticated)
    def shopping_list(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user).all()
        shopping_list = {}
        for item in shopping_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                name = recipe_ingredient.ingredient.name
                measurement_unit = recipe_ingredient.ingredient.measurement_unit
                amount = recipe_ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {'name': name,
                                           'measurement_unit': measurement_unit,
                                           'amount': amount}
                else:
                    shopping_list[name]['amount'] += amount
        content = [f'{item["name"]} ({item["measurement_unit"]}) - {item["amount"]}\n'
                   for item in shopping_list.values()]
        filename = 'shopping_list.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
