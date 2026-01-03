import django.core.exceptions
import django.test
import parameterized

import catalog.models
import catalog.tests.factories


class ValidateMustContainValidatorTests(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = catalog.tests.factories.CategoryFactory()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Category.objects.all().delete()
        super().tearDown()

    @parameterized.parameterized.expand(
        [
            ('excellent'),
            ('EXCELLENT'),
            ('excellent!'),
            ('luxurious'),
            ('LUXURIOUS'),
            ('luxurious?'),
        ],
    )
    def test_item_validate_must_contain_validator_positive(self, text):
        count = catalog.models.Item.objects.count()

        item = catalog.tests.factories.ItemFactory.build(
            text=text,
            category=self.category,
        )

        item.full_clean()
        item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            count + 1,
            'The number of Item objects should have increased by 1 '
            f'for text "{text}".',
        )

    @parameterized.parameterized.expand(
        [
            ('luxury'),
            ('excellently'),
            ('good'),
            ('luxuriou'),
            ('excellen'),
            ('123excellent'),
            ('luxurious123'),
            ('ex cellent'),
            ('12345'),
            ('!@#$%'),
            (''),
        ],
    )
    def test_item_validate_must_contain_validator_negative(self, text):
        count = catalog.models.Item.objects.count()

        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg=(
                f'A ValidationError should have been raised for text "{text}".'
            ),
        ):
            item = catalog.tests.factories.ItemFactory.build(
                text=text,
                category=self.category,
            )
            item.full_clean()
            item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            count,
            (
                'The number of Item objects should not have changed '
                f'for invalid text "{text}".'
            ),
        )
