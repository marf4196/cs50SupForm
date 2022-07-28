from rest_framework.views import APIView
from .serializer import CheckTokenSerializer, SupportersSurveySerializers
from web.models import SupportSurveyCounter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

class CheckToken(APIView):
    """
        api/v1/check_token/
        this endpoint gets an token via json and checks if it's valid or not.
    """
    serializer_class = CheckTokenSerializer
    
    def post(self, request):
        survey_max_capacity = 5
        serializer = CheckTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        try:
            user = SupportSurveyCounter.objects.get(student__ticket=token)
        
        # check to see if the user token is registered in database or not
        except SupportSurveyCounter.DoesNotExist:
            return Response({"error": "این کد ایوند در دیتابیس دانشجویان دوره مبانی یافت نشد"}, status=HTTP_400_BAD_REQUEST)

        # user is not allowed to submit more than 5 survey in a week
        if user.survey_counter + 1 > survey_max_capacity:
            return Response({"error":"شما نمی توانید بیشتر از ۵ بار در هفته ثبت نظر داشته باشید"}, status=HTTP_400_BAD_REQUEST)

        # TODO: MOVE THIS INTO SubmitSupportersSurvey
        else: # everything is fine
            user.survey_counter += 1
            user.save()
            return Response({"success": "نظر شما با موفقیت ثبت شد"}, status=HTTP_200_OK)

class SubmitSupportersSurvey(APIView):
    serializer_class = SupportersSurveySerializers
    
    def post(self, request):
        serializer = SupportersSurveySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "نظر شما با موفقیت ثبت شد"}, status=HTTP_200_OK)