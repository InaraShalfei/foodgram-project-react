import imghdr

import webcolors as webcolors
from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
import six
import uuid

from api.models import Ingredient, Recipe, Tag


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
            complete_file_name = "%s.%s" % (file_name, file_extension, )
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
        fields = ('name', 'id', 'measurement_unit')
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = ('name', 'ingredients', 'tags', 'text', 'image', 'cooking_time')
        model = Recipe
