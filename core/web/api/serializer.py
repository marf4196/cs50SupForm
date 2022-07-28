from rest_framework import serializers
from web.models import SupporterSurvey

class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, required=True)

class SupporterSurveySerializers(serializers.ModelSerializer):
    class Meta:
        model = SupporterSurvey
        fields = ['name', 'token', 'supporter', 'validate_status', 'description', 'image']
    