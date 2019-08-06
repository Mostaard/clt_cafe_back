from enum import Enum


class ErrorCode(Enum):
    LANGUAGE_CODE = 'INVALID_LANGUAGE_CODE'
    TRANSLATION = 'TRANSLATION'

    def __str__(self):
        return 'LNG' + self.value
