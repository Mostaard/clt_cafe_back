from django.core.exceptions import ValidationError
from django.test import TestCase

from clt_cafe_back.apps.languages.language_codes import LanguageCode
from clt_cafe_back.apps.languages.models import Language


class LanguageTest(TestCase):
    def test_multilingual_name(self):
        language = Language.objects.create(language_code=LanguageCode.FRENCH,
                                           name={str(LanguageCode.DUTCH): 'Frans',
                                                 str(LanguageCode.FRENCH): 'Français'})
        name = language.name[str(LanguageCode.DUTCH)]
        self.assertEqual('Frans', name)

    def test_non_language_code_number(self):
        with self.assertRaises(ValidationError) as e:
            Language.objects.create(language_code=LanguageCode.DUTCH, name={str(LanguageCode.DUTCH): 1})
        self.assertIn('is an invalid translation', e.exception.messages[0])

    def test_non_language_code_object(self):
        with self.assertRaises(ValidationError) as e:
            Language.objects.create(language_code=LanguageCode.DUTCH, name={str(LanguageCode.DUTCH): {'five': '5'}})
        self.assertIn('is an invalid translation', e.exception.messages[0])
