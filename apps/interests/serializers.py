from rest_framework import serializers

from clt_cafe_back.apps.interests.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['name', 'description']
