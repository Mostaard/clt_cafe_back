from django.test import TestCase
from rest_framework.test import APIClient

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.interests.models import Interest
from clt_cafe_back.apps.languages.language_codes import LanguageCode


def get_json_interest():
    return {'name': {str(LanguageCode.DUTCH): 'Sport',
                     str(LanguageCode.ENGLISH): 'Sport'},
            'description': {str(LanguageCode.DUTCH): 'Je sport graag',
                            str(LanguageCode.ENGLISH): 'You like sports'}
            }


class BaseTest(TestCase):
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
