import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Category)
class Category(django.contrib.admin.ModelAdmin):
    model = catalog.models.Category


@django.contrib.admin.register(catalog.models.Tag)
class Tag(django.contrib.admin.ModelAdmin):
    model = catalog.models.Tag


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    readonly_fields = (
        catalog.models.Item.updated_at.field.name,
        catalog.models.Item.created_at.field.name,
    )

    item_fields = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.name.field.name,
        catalog.models.Item.category.field.name,
        catalog.models.Item.tags.field.name,
        catalog.models.Item.updated_at.field.name,
        catalog.models.Item.created_at.field.name,
    )

    description_fields = (catalog.models.Item.text.field.name,)

    fieldsets = (
        (None, {'fields': item_fields}),
        ('Description', {'fields': description_fields}),
    )
