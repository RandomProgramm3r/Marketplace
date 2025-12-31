import django.core.exceptions
import django.test
import parameterized

import catalog.tests.factories


class CategoryModelTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            (-100, 'Ensure validation fails when weight is negative'),
            (0, 'Ensure validation fails when weight is less than 1'),
            (
                32768,
                'Ensure validation fails when weight is greater than 32767',
            ),
        ],
    )
    def test_category_weight_validation(self, weight, msg):
        category = catalog.tests.factories.CategoryFactory.build(weight=weight)

        with self.assertRaises(django.core.exceptions.ValidationError) as exc:
            category.full_clean()

        self.assertIn('weight', exc.exception.message_dict, msg=msg)

    @parameterized.parameterized.expand(
        [
            (1, 'Ensure validation passes when weight is 1 (min value)'),
            (100, 'Ensure validation passes when weight is 100'),
            (
                32767,
                'Ensure validation passes when weight is 32767 (max value)',
            ),
        ],
    )
    def test_category_weight_is_valid(self, weight, msg):
        category = catalog.tests.factories.CategoryFactory.build(weight=weight)

        try:
            category.full_clean()
        except django.core.exceptions.ValidationError as e:
            self.fail(
                f'Validation failed unexpectedly for weight {weight}: {e}',
            )
