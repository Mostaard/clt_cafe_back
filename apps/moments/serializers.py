from rest_framework import serializers

from clt_cafe_back.apps.moments.models import Moment


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = ['language', 'level']
