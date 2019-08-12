from unittest import TestCase
from rest_framework.test import APIClient

from clt_cafe_back.apps.accounts.models import User


class MomentTest(TestCase):

    def setUp(self):
        self.john = User.objects.create_user(username="john")
        self.gertrude = User.objects.create_user(username="gertrude")
        self.client = APIClient()
        self.client.force_authenticate(user=self.john)

    def test_get_moments(self):
        response = self.client.get('/languages/', follow=True)
        self.assertEqual(response.status_code, 200)
