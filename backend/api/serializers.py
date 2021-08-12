import imghdr
import base64
import six
import uuid
import webcolors as webcolors

from rest_framework import serializers
from django.core.files.base import ContentFile

from api.models import Ingredient, Recipe, Tag, RecipeIngredient, FavoriteRecipe, ShoppingCart
from users.mixins import IsSubscribedMixin
from users.models import User
from users.serializers import CustomUserSerializer


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        fields = ('name', 'slug', 'id', 'color')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(read_only=True, source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientReadSerializer(many=True, read_only=True, source='recipe_ingredients')
    tags = serializers.SlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='slug')
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')

    class Meta:
        fields = ('id', 'author', 'name', 'ingredients', 'tags', 'text', 'image',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart')
        model = Recipe

    def get_is_favorited(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj, user=self.context.get('user')).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(recipe=obj, user=self.context.get('user')).exists()


class RecipeShortRead(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'cooking_time', 'name', 'image')
        model = Recipe


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        exclude = ['author']

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=self.context.get('user'), **validated_data)
        for item in ingredients:
            RecipeIngredient.objects.create(amount=item.pop('amount'), ingredient=item.pop('id'), recipe=recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for item in ingredients:
            RecipeIngredient.objects.create(amount=item.pop('amount'), ingredient=item.pop('id'), recipe=instance)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.tags.set(tags)
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='recipe.id')
    cooking_time = serializers.CharField(read_only=True, source='recipe.cooking_time')
    image = serializers.CharField(read_only=True, source='recipe.image')
    name = serializers.CharField(read_only=True, source='recipe.name')

    class Meta:
        fields = ('id', 'cooking_time', 'name', 'image')
        model = FavoriteRecipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='recipe.id')
    cooking_time = serializers.CharField(read_only=True, source='recipe.cooking_time')
    image = serializers.CharField(read_only=True, source='recipe.image')
    name = serializers.CharField(read_only=True, source='recipe.name')

    class Meta:
        fields = ('id', 'cooking_time', 'name', 'image')
        model = ShoppingCart


class UserFollowedSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'recipes', 'recipes_count', 'is_subscribed')
        model = User

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = obj.recipes.all()[:int(recipes_limit)] if recipes_limit else obj.recipes
        serializer = serializers.ListSerializer(child=RecipeShortRead())
        return serializer.to_representation(recipes)

