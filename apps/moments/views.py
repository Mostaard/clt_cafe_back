from rest_framework import viewsets

from clt_cafe_back.apps.moments.serializers import MomentSerializer


class MomentViewSet(viewsets.ModelViewSet):
    serializer_class = MomentSerializer
