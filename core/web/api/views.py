from rest_framework.views import APIView
from .serializer import CheckTokenSerializer
from web.models import SupportSurveyHistory
from rest_framework import status
from rest_framework.response import Response

class CheckToken(APIView):
    serializer_class = CheckTokenSerializer
    
    def post(self, request):
        survey_max_capacity = 5
        serializer = self.CheckTokenSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        user = SupportSurveyHistory.objects.get_or_create(ticket=token)
        
        # user is not allowed to submit more than 5 survey in a week
        if user.counter + 1 > survey_max_capacity:
            return Response({"error":"شما نمی توانید بیشتر از ۵ بار در هفته ثبت نظر داشته باشید"}, status=status.HTTP_403_FORBIDDEN)

        else:
            user.counter += 1
            user.save()
            return Response({"success": "نظر شما با موفقیت ثبت شد"}, status=status.HTTP_200_OK)