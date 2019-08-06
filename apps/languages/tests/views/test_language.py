from clt_cafe_back.apps.languages.language_codes import LanguageCode
from clt_cafe_back.apps.languages.models import Language
from clt_cafe_back.apps.languages.tests.views.test_base import BaseApiTest


class LanguageTest(BaseApiTest):
    def test_get_languages(self):
        self.init_lanuages()
        response = self.client.get('/languages', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Language.objects.all().count())

    def test_get_language(self):
        self.init_lanuages()
        response = self.client.get('/languages/{}/'.format(str(LanguageCode.FRENCH)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'][str(LanguageCode.DUTCH)], 'Frans')
        self.assertEqual(response.data['language_code'], str(LanguageCode.FRENCH))

    def test_post_language(self):
        self.john.is_staff = True
        self.john.save()
        response = self.client.post('/languages/',
                                    data={'language_code': str(LanguageCode.FRENCH),
                                          'name': {str(LanguageCode.DUTCH): 'Frans',
                                                   str(LanguageCode.FRENCH): 'Français'}},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'][str(LanguageCode.DUTCH)], 'Frans')
        self.assertEqual(response.data['language_code'], str(LanguageCode.FRENCH))
        self.assertTrue(Language.objects.filter(language_code=str(LanguageCode.FRENCH)).exists())

    def test_post_language_unauthorized(self):
        response = self.client.post('/languages/',
                                    data={'language_code': str(LanguageCode.FRENCH),
                                          'name': {str(LanguageCode.DUTCH): 'Frans',
                                                   str(LanguageCode.FRENCH): 'Français'}},
                                    format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Language.objects.filter(language_code=str(LanguageCode.FRENCH)).exists())
