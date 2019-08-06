from clt_cafe_back.apps.languages.language_codes import LanguageCode
from clt_cafe_back.apps.languages.models import Proficiency, Language
from clt_cafe_back.apps.languages.tests.views.test_base import BaseApiTest


class ProficiencyTest(BaseApiTest):

    def test_create_proficiency(self):
        self.init_lanuages()
        dutch = Language.objects.get(language_code=LanguageCode.DUTCH)
        response = self.client.post('/proficiencies/',
                                    {'language': dutch.id, 'level': str(Proficiency.BASIC)}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['language']['name'][str(LanguageCode.DUTCH)], 'Nederlands')
        self.assertEqual(response.data['level'], str(Proficiency.BASIC))
        self.assertEqual(1, Proficiency.objects.filter(user=self.john).count())

    def test_list_proficiencies(self):
        self.init_lanuages()
        self.init_proficiencies()
        response = self.client.get('/proficiencies', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Proficiency.objects.filter(user=self.john).count())

    def test_retrieve_proficiency(self):
        self.init_lanuages()
        self.init_proficiencies()
        proficiency = Proficiency.objects.get(user=self.john, language__language_code=str(LanguageCode.GERMAN))
        response = self.client.get('/proficiencies/{}'.format(proficiency.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['language']['name']['dut'], 'Duits')
        self.assertEqual(response.data['level'], proficiency.level)

    def test_retrieve_proficiency_other_user(self):
        self.client.force_authenticate(self.gertrude)
        self.init_lanuages()
        self.init_proficiencies()
        proficiency = Proficiency.objects.get(user=self.john, language__language_code=str(LanguageCode.GERMAN))
        response = self.client.get('/proficiencies/{}'.format(proficiency.id), follow=True)
        self.assertEqual(response.status_code, 404)

    def get_proficiency(self):
        self.init_lanuages()
        self.init_proficiencies()
        return Proficiency.objects.get(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                       level=str(Proficiency.VERY_GOOD))

    def test_partial_update_proficiency(self):
        response = self.client.patch('/proficiencies/{}/'.format(self.get_proficiency().id),
                                     {'level': str(Proficiency.MOTHER_LANGUAGE)}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                                   level=str(Proficiency.MOTHER_LANGUAGE)).exists())

    def test_partial_update_proficiency_other_user(self):
        self.client.force_authenticate(self.gertrude)
        response = self.client.patch('/proficiencies/{}/'.format(self.get_proficiency().id),
                                     {'level': str(Proficiency.MOTHER_LANGUAGE)}, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                                    level=str(Proficiency.MOTHER_LANGUAGE)).exists())

    def test_update_proficiency(self):
        proficiency = self.get_proficiency()
        language = Language.objects.get(language_code=LanguageCode.DUTCH)
        response = self.client.put('/proficiencies/{}/'.format(proficiency.id),
                                   {'level': str(Proficiency.MOTHER_LANGUAGE), 'language': str(language.id)},
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.DUTCH),
                                                   level=str(Proficiency.MOTHER_LANGUAGE)).exists())

    def test_update_proficiency_other_user(self):
        self.client.force_authenticate(self.gertrude)
        proficiency = self.get_proficiency()
        language = Language.objects.get(language_code=LanguageCode.DUTCH)
        response = self.client.put('/proficiencies/{}/'.format(proficiency.id),
                                   {'level': str(Proficiency.MOTHER_LANGUAGE), 'language': str(language.id)},
                                   follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.DUTCH),
                                                    level=str(Proficiency.MOTHER_LANGUAGE)).exists())

    def test_destroy_proficiency(self):
        self.init_lanuages()
        self.init_proficiencies()
        proficiency = Proficiency.objects.get(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                              level=str(Proficiency.VERY_GOOD))
        response = self.client.delete('/proficiencies/{}/'.format(proficiency.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                                    level=str(Proficiency.VERY_GOOD)).exists())

    def test_destroy_proficiency_other_user(self):
        self.client.force_authenticate(self.gertrude)
        self.init_lanuages()
        self.init_proficiencies()
        proficiency = Proficiency.objects.get(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                              level=str(Proficiency.VERY_GOOD))
        response = self.client.delete('/proficiencies/{}/'.format(proficiency.id))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Proficiency.objects.filter(user=self.john, language__language_code=str(LanguageCode.GERMAN),
                                                   level=str(Proficiency.VERY_GOOD)).exists())
