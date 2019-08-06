from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'interests', InterestViewSet, base_name='interest')
router.register(r'user-interests', UserInterestViewSet, base_name='user-interest')
