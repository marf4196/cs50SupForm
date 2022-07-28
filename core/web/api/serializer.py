from rest_framework import serializers
from web.models import SupporterSurvey

class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, required=True)

# class SubmitSupportersSurveySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupporterSurvey
#         fields = "__all__"

#     def validate(self, attrs):
#         form = SupportersSurveyForm(a)

class SupportersSurveySerializers(serializers.ModelSerializer):
    class Meta:
        model = SupporterSurvey
        fields = ['name', 'token', 'supporter', 'status', 'description', 'image']
    