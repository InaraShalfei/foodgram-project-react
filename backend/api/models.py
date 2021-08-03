from django.core.validators import MinLengthValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='name', unique=True)
    slug = models.SlugField(max_length=100, verbose_name='slug', unique=True)
    color = models.CharField(max_length=100, verbose_name='color', unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug'
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='name', unique=True)
    measurement_unit = models.CharField(max_length=20, verbose_name='measuring unit', unique=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='name', unique=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    text = models.TextField(max_length=1000, verbose_name='description')
    cooking_time = models.IntegerField(verbose_name='time', validators=[MinLengthValidator(1)])
    image = models.ImageField(upload_to='media')

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name
