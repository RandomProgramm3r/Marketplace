import django.test
import parameterized

import catalog.models


class PublishedWithNameBaseModelTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ('Short name', 'Short name'),
            ('A name strictly 15 chars', 'A name strictly'),
            ('A very long name that needs truncation', 'A very long nam'),
        ],
    )
    def test_string_representation_truncation(self, name, expected_str):
        tag = catalog.models.Tag(name=name)

        self.assertEqual(
            str(tag),
            expected_str,
            msg=f"Expected __str__ to be '{expected_str}' for name '{name}'",
        )
