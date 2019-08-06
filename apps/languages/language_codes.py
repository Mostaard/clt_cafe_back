from enum import Enum


class LanguageCode(Enum):
    ARABIC = 'ara'
    BULGARIAN = 'bul'
    CHINESE = 'chi'
    DANISH = 'dan'
    DUTCH = 'dut'
    ENGLISH = 'eng'
    FINNISH = 'fin'
    FRENCH = 'fra'
    GERMAN = 'deu'
    GREEK = 'ell'
    HUNGARIAN = 'hun'
    ITALIAN = 'ita'
    JAPANESE = 'jpn'
    NORWEGIAN = 'nor'
    POLISH = 'pol'
    PORTUGUESE = 'por'
    ROMANIAN = 'rum'
    RUSSIAN = 'rus'
    SPANISH = 'spa'
    SWEDISH = 'swe'
    TURKISH = 'tur'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def __str__(self):
        return self.value

