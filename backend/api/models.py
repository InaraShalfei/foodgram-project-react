from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=100, verbose_name='slug', unique=True)
    color = models.CharField(max_length=100, verbose_name='color')

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
