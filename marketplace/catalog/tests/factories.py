import factory
import marketplace.utils.tests.base

import catalog.models


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = catalog.models.Tag

    name = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.word(),
    )

    slug = factory.Sequence(
        lambda n: f'tag-{n}-{marketplace.utils.tests.base.faker.slug()}',
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = catalog.models.Category

    name = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.word(),
    )
    slug = factory.Sequence(
        lambda n: f'category-{n}-{marketplace.utils.tests.base.faker.slug()}',
    )

    weight = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.random_int(
            min=1,
            max=32767,
        ),
    )


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = catalog.models.Item

    name = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.sentence(nb_words=3),
    )
    text = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.text(),
    )

    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
