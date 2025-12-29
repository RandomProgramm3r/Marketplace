import django.db.models


class PublishedWithNameBaseModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        'published',
        default=True,
    )
    name = django.db.models.CharField(
        'name',
        max_length=150,
        unique=True,
        help_text='Maximum 150 characters.',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self._short_name()

    def _short_name(self):
        return self.name[:15]
