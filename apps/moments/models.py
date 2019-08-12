from datetime import datetime

from django.db import models

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.locations.models import Location


def find_moments(from_datetime: datetime, until_datetime: datetime, user: User):
    languages = [proficiency.language for proficiency in user.proficiencies.all()]
    return Moment.objects.filter(start__gte=from_datetime, start__lte=until_datetime,
                                 participants__proficiencies__language__in=languages)


class Moment(models.Model):
    start = models.DateTimeField()
    participants = models.ManyToManyField(User)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    min_participants = models.PositiveIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)


class ParticipationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participation_requests')
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name='participation_requests')
