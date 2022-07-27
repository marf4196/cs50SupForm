from urllib import request
from rest_framework import serializers

class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, required=True)
