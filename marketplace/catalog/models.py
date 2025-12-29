import django.core.validators
import django.db.models

import core.models


class Tag(core.models.PublishedWithNameBaseModel):
    slug = django.db.models.SlugField(
        'slug',
        max_length=200,
        unique=True,
        help_text='Maximum 200 characters.',
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Category(core.models.PublishedWithNameBaseModel):
    slug = django.db.models.SlugField(
        'slug',
        max_length=200,
        unique=True,
        help_text='Maximum 200 characters.',
    )
    weight = django.db.models.PositiveSmallIntegerField(
        'weight',
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Item(core.models.PublishedWithNameBaseModel):
    category = django.db.models.ForeignKey(
        Category,
        verbose_name='category',
        on_delete=django.db.models.CASCADE,
        related_query_name='item',
        help_text='Select a category for the item',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='tags',
        related_query_name='item',
        help_text='Select tags for the item',
    )
    text = django.db.models.TextField(
        'text',
    )

    created_at = django.db.models.DateTimeField(
        'creation date',
        db_index=True,
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField('update date', auto_now=True)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        default_related_name = 'items'
