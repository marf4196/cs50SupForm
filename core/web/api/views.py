from email.mime import image
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .serializer import SupportSurveySerializer
from web.models import Students, SupporterSurvey

class SupportSurvey(APIView):
    serializer_class = SupportSurveySerializer
    permission_classes = ()
    authentication_classes = ()
    def post(self, request, *args, **kwargs):
        serializer = SupportSurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True})