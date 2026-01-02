import re

import django.core.exceptions
import django.utils.deconstruct

WORDS_PATTERN = re.compile(r'\w+|\W+')


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.validated_words = {word.lower() for word in args}

    def __call__(self, value):
        words = set(WORDS_PATTERN.findall(value.lower()))

        if not words & self.validated_words:
            raise django.core.exceptions.ValidationError(
                (
                    'The text must contain at least one of the words: '
                    f'{", ".join(self.validated_words)}.',
                ),
            )
