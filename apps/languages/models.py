from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from gettext import gettext as _

from clt_cafe_back.apps.accounts.models import User
from clt_cafe_back.apps.languages.error_codes import ErrorCode
from clt_cafe_back.apps.languages.language_codes import LanguageCode


class MultiLanguageField(JSONField):
    def validate(self, value, model_instance):
        for language_code in value.keys():
            self.validate_language_code(language_code)
            self.validate_translation(language_code, value)
            super().validate(value, model_instance)

    @staticmethod
    def validate_translation(language_code, value):
        if not isinstance(value.get(language_code), str):
            raise ValidationError(
                message=_('{} is an invalid translation'.format(value.get(language_code))),
                code=ErrorCode.TRANSLATION,
            )

    @staticmethod
    def validate_language_code(language_code):
        if not LanguageCode.has_value(language_code):
            raise ValidationError(
                message=_('{} is an invalid language code'.format(language_code)),
                code=ErrorCode.LANGUAGE_CODE,
            )


class Language(models.Model):
    name = MultiLanguageField()
    language_code = models.CharField(max_length=3, unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)


class Proficiency(models.Model):
    BASIC = 'B'
    GOOD = 'G'
    VERY_GOOD = 'V'
    MOTHER_LANGUAGE = 'M'
    LEVEL_CHOICES = [
        (BASIC, _('Basic')),
        (GOOD, _('Good')),
        (VERY_GOOD, _('Very good')),
        (MOTHER_LANGUAGE, _('Mother language')),
    ]

    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    level = models.CharField(
        max_length=1,
        choices=LEVEL_CHOICES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proficiencies')
    is_learning = models.BooleanField(default=True)
