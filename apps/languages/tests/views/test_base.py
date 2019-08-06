from django.test import TestCase
from rest_framework.test import APIClient

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.languages.language_codes import LanguageCode
from clt_cafe_back.apps.languages.models import Language, Proficiency


class BaseApiTest(TestCase):
    def setUp(self):
        self.john = User.objects.create_user(username="john")
        self.gertrude = User.objects.create_user(username="gertrude")
        self.client = APIClient()
        self.client.force_authenticate(user=self.john)

    def init_lanuages(self):
        Language.objects.create(language_code=LanguageCode.FRENCH,
                                name={str(LanguageCode.DUTCH): 'Frans',
                                      str(LanguageCode.FRENCH): 'Français',
                                      str(LanguageCode.ENGLISH): 'French'})
        Language.objects.create(language_code=LanguageCode.DUTCH,
                                name={str(LanguageCode.DUTCH): 'Nederlands',
                                      str(LanguageCode.FRENCH): 'Néerlandais',
                                      str(LanguageCode.ENGLISH): 'Dutch'})
        Language.objects.create(language_code=LanguageCode.ENGLISH,
                                name={str(LanguageCode.DUTCH): 'Engels',
                                      str(LanguageCode.FRENCH): 'Anglais',
                                      str(LanguageCode.ENGLISH): 'English'})
        Language.objects.create(language_code=LanguageCode.GERMAN,
                                name={str(LanguageCode.DUTCH): 'Duits',
                                      str(LanguageCode.FRENCH): 'Allemand',
                                      str(LanguageCode.ENGLISH): 'German'})

    def init_proficiencies(self):
        Proficiency.objects.create(language=Language.objects.get(language_code=str(LanguageCode.GERMAN)),
                                   level=Proficiency.VERY_GOOD,
                                   user=self.john)
        Proficiency.objects.create(language=Language.objects.get(language_code=str(LanguageCode.ENGLISH)),
                                   level=Proficiency.MOTHER_LANGUAGE,
                                   user=self.john)
        Proficiency.objects.create(language=Language.objects.get(language_code=str(LanguageCode.FRENCH)),
                                   level=Proficiency.BASIC,
                                   user=self.john)
        Proficiency.objects.create(language=Language.objects.get(language_code=str(LanguageCode.GERMAN)),
                                   level=Proficiency.MOTHER_LANGUAGE,
                                   user=self.gertrude)
        Proficiency.objects.create(language=Language.objects.get(language_code=str(LanguageCode.DUTCH)),
                                   level=Proficiency.BASIC,
                                   user=self.gertrude)
