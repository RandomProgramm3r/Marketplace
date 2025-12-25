import re

import django.conf

ENGLISH_LETTERS_PATTERN = re.compile(r'^[A-Za-z]+$')
WORDS_PATTERN = re.compile(r'\w+|\W+')


class ReverseEnglishWordsMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def check_need_reverse(self):
        if not django.conf.settings.ALLOW_REVERSE:
            return False

        ReverseEnglishWordsMiddleware.count += 1
        if ReverseEnglishWordsMiddleware.count != 10:
            return False

        ReverseEnglishWordsMiddleware.count = 0

        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        response.content = self.reverse_english_words(response.text).encode()

        return response

    def reverse_english_words(self, content):
        words = WORDS_PATTERN.findall(content)

        reversed_words = [
            word[::-1] if ENGLISH_LETTERS_PATTERN.match(word) else word
            for word in words
        ]

        return ''.join(reversed_words)
