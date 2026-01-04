import factory
import marketplace.utils.tests.base

import core.models


class PublishedWithNameBaseModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = core.models.PublishedWithNameBaseModel
        abstract = True

    name = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.word(),
    )
    is_published = True
