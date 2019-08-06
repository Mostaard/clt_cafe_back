from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import LanguageSerializer, ProficiencySerializer
from .models import Language, Proficiency


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'language_code'
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProficiencyViewSet(viewsets.ModelViewSet):
    serializer_class = ProficiencySerializer
    pagination_class = None

    def get_queryset(self):
        return Proficiency.objects.filter(user=self.request.user)
