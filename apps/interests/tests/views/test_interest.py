from django.test import TestCase
from rest_framework.test import APIClient

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.interests.models import Interest
from clt_cafe_back.apps.languages.language_codes import LanguageCode


def get_json_interest():
    return {'name': {str(LanguageCode.DUTCH): 'Lezen',
                     str(LanguageCode.ENGLISH): 'Reading'},
            'description': {str(LanguageCode.DUTCH): 'Je leest graag',
                            str(LanguageCode.ENGLISH): 'You like reading'}
            }


class InterestTest(TestCase):

    def setUp(self):
        self.john = User.objects.create_user(username="john", is_staff=True)
        self.gertrude = User.objects.create_user(username="gertrude")
        self.client = APIClient()
        self.client.force_authenticate(user=self.john)
        self.interests = []

    def create_interests(self):
        self.interests.append(Interest.objects.create(name={str(LanguageCode.ENGLISH): 'Reading'},
                                                      description={str(LanguageCode.ENGLISH): 'You like to read'}))
        self.interests.append(Interest.objects.create(name={str(LanguageCode.ENGLISH): 'Yoga'},
                                                      description={
                                                          str(LanguageCode.ENGLISH): 'The art of bending the body'}))

    def test_create_interest(self):
        response = self.client.post('/interests/', get_json_interest(), format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Interest.objects.count(), 1)
        self.assertEqual(Interest.objects.all()[0].description, {str(LanguageCode.DUTCH): 'Je leest graag',
                                                                 str(LanguageCode.ENGLISH): 'You like reading'})
        self.assertEqual(Interest.objects.all()[0].name, {str(LanguageCode.DUTCH): 'Lezen',
                                                          str(LanguageCode.ENGLISH): 'Reading'})

    def test_create_interest_unauthorized(self):
        self.client.force_authenticate(self.gertrude)
        response = self.client.post('/interests/', get_json_interest(), format='json')
        self.assertEqual(response.status_code, 403)

    def test_list_interests(self):
        self.client.force_authenticate(self.gertrude)
        self.create_interests()
        response = self.client.get('/interests/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Interest.objects.count())

    def test_retrieve_interest(self):
        self.client.force_authenticate(self.gertrude)
        self.create_interests()
        response = self.client.get('/interests/{}'.format(self.interests[0].id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.interests[0].name, response.data['name'])

    def test_partial_update_interest(self):
        self.create_interests()
        description = self.interests[0].description
        description[str(LanguageCode.DUTCH)] = 'Je leest graag'
        response = self.client.patch('/interests/{}/'.format(self.interests[0].id), {'description': description},
                                     format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], description)
        self.assertEqual(Interest.objects.get(id=self.interests[0].id).description, description)

    def test_partial_update_interest_unauthorized(self):
        self.client.force_authenticate(self.gertrude)
        self.create_interests()
        response = self.client.patch('/interests/{}/'.format(self.interests[0].id), {'description': {}},
                                     format='json', follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Interest.objects.get(id=self.interests[0].id).description, {})

    def test_update_interest(self):
        self.create_interests()
        description = self.interests[0].description
        name = self.interests[0].name
        description[str(LanguageCode.DUTCH)] = 'Je leest graag'
        name[str(LanguageCode.DUTCH)] = 'Lezen'
        response = self.client.patch('/interests/{}/'.format(self.interests[0].id),
                                     {'description': description, 'name': name},
                                     format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], description)
        self.assertEqual(Interest.objects.get(id=self.interests[0].id).description, description)
        self.assertEqual(response.data['name'], name)
        self.assertEqual(Interest.objects.get(id=self.interests[0].id).name, name)

    def test_update_interest_unauthorized(self):
        self.client.force_authenticate(self.gertrude)
        self.create_interests()
        response = self.client.patch('/interests/{}/'.format(self.interests[0].id),
                                     {'description': {}, 'name': {}},
                                     format='json', follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Interest.objects.get(id=self.interests[0].id).description, {})
        self.assertNotEqual(Interest.objects.get(id=self.interests[0].id).name, {})

    def test_destroy_interest(self):
        self.create_interests()
        response = self.client.delete('/interests/{}/'.format(self.interests[0].id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Interest.objects.filter(pk=self.interests[0].id).exists())

    def test_destroy_interest_unauthorized(self):
        self.client.force_authenticate(self.gertrude)
        self.create_interests()
        response = self.client.delete('/interests/{}/'.format(self.interests[0].id))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Interest.objects.filter(pk=self.interests[0].id).exists())
