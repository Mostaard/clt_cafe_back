from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from clt_cafe_back.apps.languages.urls import router as language_router
from clt_cafe_back.apps.interests.urls import router as interest_router


router = routers.DefaultRouter()
router.registry.extend(language_router.registry)
router.registry.extend(interest_router.registry)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
