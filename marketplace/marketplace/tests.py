import collections

import django.test
import django.urls
import parameterized

import marketplace.middleware


class ReverseEnglishWordsMiddlewareTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.middleware_instance = (
            marketplace.middleware.ReverseEnglishWordsMiddleware(
                get_response=None,
            )
        )
        cls.coffee_url = django.urls.reverse('homepage:coffee')

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_english_words_enabled(self):
        responses = [
            django.test.Client().get(self.coffee_url).content
            for _ in range(10)
        ]
        contents = collections.Counter(responses)

        self.assertEqual(
            len(contents),
            2,
            'There must be two answer options: normal and reversed.',
        )
        self.assertEqual(
            contents.most_common(),
            [("I'm a Teapot".encode(), 9), ("I'm a topaeT".encode(), 1)],
            (
                'The distribution of answers is incorrect: '
                'expected 9 normal and 1 reversed.'
            ),
        )
        self.assertIn(
            "I'm a Teapot".encode(),
            contents,
            'The normal answer must be present in the responses.',
        )
        self.assertIn(
            "I'm a topaeT".encode(),
            contents,
            'The reversed answer must be present in the responses.',
        )

        response = django.test.Client().get(
            django.urls.reverse('homepage:coffee'),
        )
        self.assertEqual(
            response.content,
            "I'm a Teapot".encode(),
            'The 11th request must return normal (not reversed) content.',
        )

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_reverse_english_words_disabled(self):
        responses = [
            django.test.Client().get(self.coffee_url).content
            for _ in range(10)
        ]
        contents = collections.Counter(responses)

        self.assertEqual(
            len(contents),
            1,
            (
                'There must be only one answer option '
                'when reversal is disabled.'
            ),
        )
        self.assertEqual(
            contents.most_common(),
            [("I'm a Teapot".encode(), 10)],
            'All 10 answers must be normal (not reversed).',
        )
        self.assertIn(
            "I'm a Teapot".encode(),
            contents,
            'The normal answer must be present.',
        )
        self.assertNotIn(
            "I'm a topaeT".encode(),
            contents,
            (
                'The reversed answer must not appear '
                'when the function is disabled.'
            ),
        )

    def test_reverse_english_words_default_setting(self):
        responses = [
            django.test.Client().get(self.coffee_url).content
            for _ in range(10)
        ]
        contents = collections.Counter(responses)

        self.assertEqual(
            len(contents),
            2,
            'By default, there must be two answer options.',
        )
        self.assertEqual(
            contents.most_common(),
            [
                ("I'm a Teapot".encode(), 9),
                ("I'm a topaeT".encode(), 1),
            ],
            (
                'The default distribution is incorrect: '
                'expected 9 normal and 1 reversed.'
            ),
        )
        self.assertIn(
            "I'm a Teapot".encode(),
            contents,
            'The normal answer must be present by default.',
        )
        self.assertIn(
            "I'm a topaeT".encode(),
            contents,
            'The reversed answer must be present by default.',
        )

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_english_words_periodicity(self):
        responses = [
            django.test.Client().get(self.coffee_url).content
            for _ in range(30)
        ]
        contents = collections.Counter(responses)

        self.assertEqual(
            len(contents),
            2,
            'There must be only 2 answer options across 30 requests.',
        )
        self.assertEqual(
            contents.most_common(),
            [
                ("I'm a Teapot".encode(), 27),
                ("I'm a topaeT".encode(), 3),
            ],
            (
                'The distribution across 30 requests is incorrect: '
                'expected 27 normal and 3 reversed.'
            ),
        )
        self.assertIn(
            "I'm a Teapot".encode(),
            contents,
            'The normal answer must be present in the series of 30 requests.',
        )
        self.assertIn(
            "I'm a topaeT".encode(),
            contents,
            (
                'The reversed answer must be present '
                'in the series of 30 requests.'
            ),
        )

    @parameterized.parameterized.expand(
        [
            ('Hello - world ★', 'olleH - dlrow ★'),
            (
                'lorem ipsum, dolor sit.',
                'merol muspi, rolod tis.',
            ),
            (
                'Multi-line - is good.',
                'itluM-enil - si doog.',
            ),
            (
                'One тест, two теста and english-text!',
                'enO тест, owt теста dna hsilgne-txet!',
            ),
            (
                '(Abc) [Def] {ghi} `jkl`',
                '(cbA) [feD] {ihg} `lkj`',
            ),
            ('user123', 'user123'),
            (
                'Latin日本語',
                'Latin日本語',
            ),
            ('What?!?!', 'tahW?!?!'),
            ('[Input] (output)', '[tupnI] (tuptuo)'),
            (
                'Some random text with email@, such a ♥case... Test¡ 1234',
                'emoS modnar txet htiw liame@, hcus a ♥esac... tseT¡ 1234',
            ),
        ],
    )
    def test_reverse_english_words(self, content, expected):
        result = self.middleware_instance.reverse_english_words(content)
        self.assertEqual(
            result,
            expected,
            f'Error when reversing string: "{content}"',
        )
