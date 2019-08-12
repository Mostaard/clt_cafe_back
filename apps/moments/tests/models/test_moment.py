from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.languages.language_codes import LanguageCode
from clt_cafe_back.apps.languages.models import Language, Proficiency
from clt_cafe_back.apps.moments.models import find_moments, Moment


class MomentTest(TestCase):
    def test_find_moments(self):
        self.john = User.objects.create_user(username="john")
        self.gertrude = User.objects.create_user(username="gertrude")

        french = Language.objects.create(language_code=LanguageCode.FRENCH,
                                         name={str(LanguageCode.DUTCH): 'Frans'})
        Proficiency.objects.create(language=french,
                                   level=Proficiency.VERY_GOOD,
                                   user=self.john)
        Proficiency.objects.create(language=french,
                                   level=Proficiency.BASIC,
                                   user=self.gertrude)

        moments = [Moment.objects.create(start=timezone.now() + timedelta(hours=2)),
                   Moment.objects.create(start=timezone.now() + timedelta(hours=5)),
                   Moment.objects.create(start=timezone.now() + timedelta(hours=8)),
                   Moment.objects.create(start=timezone.now() + timedelta(hours=9))]
        moments[0].participants.add(self.gertrude)
        moments[1].participants.add(self.john)

        found_moments = find_moments(from_datetime=timezone.now(), until_datetime=timezone.now() + timedelta(days=1),
                                     user=self.john)
        self.assertEqual(len(found_moments), 1)
