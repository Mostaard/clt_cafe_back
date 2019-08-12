from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'moments', MomentViewSet, base_name='moment')
