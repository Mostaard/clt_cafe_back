from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from clt_cafe_back.apps.interests.models import Interest
from clt_cafe_back.apps.interests.serializers import InterestSerializer


class InterestViewSet(viewsets.ModelViewSet):
    serializer_class = InterestSerializer
    pagination_class = None
    queryset = Interest.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated] if self.action in ['list', 'retrieve'] else [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserInterestViewSet(viewsets.ModelViewSet):
    serializer_class = InterestSerializer
    pagination_class = None

    def get_queryset(self):
        Interest.objects.filter(users=self.request.user)
