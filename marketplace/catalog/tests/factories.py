import factory
import marketplace.utils.tests.base

import catalog.models
import core.tests.factories


class TagFactory(core.tests.factories.PublishedWithNameBaseModelFactory):
    class Meta:
        model = catalog.models.Tag

    slug = factory.Sequence(
        lambda n: f'tag-{n}-{marketplace.utils.tests.base.faker.slug()}',
    )


class CategoryFactory(core.tests.factories.PublishedWithNameBaseModelFactory):
    class Meta:
        model = catalog.models.Category

    slug = factory.Sequence(
        lambda n: f'category-{n}-{marketplace.utils.tests.base.faker.slug()}',
    )

    weight = factory.LazyAttribute(
        lambda _: marketplace.utils.tests.base.faker.random_int(
            min=1,
            max=32767,
        ),
    )


class ItemFactory(core.tests.factories.PublishedWithNameBaseModelFactory):
    class Meta:
        model = catalog.models.Item

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
