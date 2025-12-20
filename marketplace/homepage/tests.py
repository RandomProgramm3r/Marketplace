import http

import django.test
import django.urls


class HomepageURLTests(django.test.TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.coffee_url = django.urls.reverse('homepage:coffee')

    def test_coffee_url_is_available(self):
        response = self.client.get(self.coffee_url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
            (f'The page {self.coffee_url}should return status 418.'),
        )

    def test_coffee_url_returns_correct_content(self):
        response = self.client.get(self.coffee_url)
        self.assertIn(
            "I'm a Teapot",
            response.text,
            msg=(
                'The page /coffee/ is missing the expected text '
                '"I\'m a Teapot".'
            ),
        )
