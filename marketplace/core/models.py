import re

import django.core.exceptions
import django.db.models
import unidecode

ONLY_LETTERS_PATTERN = re.compile(r'[^a-zA-Z]')


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
    canonical_name = django.db.models.CharField(
        'canonical name',
        max_length=150,
        unique=True,
        editable=False,
        help_text='Canonical name',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self._short_name()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._generate_canonical_name()

        if not self.canonical_name:
            raise django.core.exceptions.ValidationError(
                'The name cannot consist entirely of special characters.',
            )

        if (
            self.__class__.objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                ('An object with this or a very similar name already exists.'),
            )

    def _generate_canonical_name(self):
        ascii_name = unidecode.unidecode(self.name)

        letters_only = re.sub(ONLY_LETTERS_PATTERN, '', ascii_name)

        return letters_only.lower()

    def _short_name(self):
        return self.name[:15]
