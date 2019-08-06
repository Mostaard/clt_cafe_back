from django.db import models

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.languages.models import MultiLanguageField


class Interest(models.Model):
    name = MultiLanguageField()
    description = MultiLanguageField()
    users = models.ManyToManyField(User)
