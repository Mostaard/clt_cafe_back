from django.test import TestCase

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.interests.models import Interest
from clt_cafe_back.apps.languages.language_codes import LanguageCode


class InterestTest(TestCase):
    def test_m2m_users(self):
        interest = Interest.objects.create(name={str(LanguageCode.ENGLISH): 'Yoga'},
                                           description={str(LanguageCode.ENGLISH): 'The art of bending the body'})
        john = User.objects.create_user(username="john")
        gertrude = User.objects.create_user(username="gertrude")
        interest.users.add(john)
        interest.users.add(gertrude)
        interest.users.add(gertrude)
        self.assertEqual(Interest.objects.all().count(), 1)
        self.assertEqual(interest.users.count(), 2)
