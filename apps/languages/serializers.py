from rest_framework import serializers

from .models import Language, Proficiency


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ProficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proficiency
        fields = ['language', 'level']

    def create(self, validated_data):
        return Proficiency.objects.create(user=self.context['request'].user,
                                          language=validated_data['language'],
                                          level=validated_data['level'])

    def to_representation(self, proficiency):
        self.fields['language'] = LanguageSerializer()
        return super().to_representation(proficiency)
