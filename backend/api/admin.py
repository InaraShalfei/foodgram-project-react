from django.contrib import admin

from users.models import User
from .models import Ingredient, Tag, Recipe, RecipeIngredient


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    inlines = (RecipeIngredientInline, )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline,)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(RecipeIngredient)
