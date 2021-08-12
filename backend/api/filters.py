import django_filters

from .models import Tag, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    author = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
