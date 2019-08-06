from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'languages', LanguageViewSet, base_name='language')
router.register(r'proficiencies', ProficiencyViewSet, base_name='proficiency')
