from django.urls import path
from .views import CheckToken, SubmitSupportersSurvey

urlpatterns = [
    path('check_token/', CheckToken.as_view(), name='check_token'),
    path('submit_supporters_survey/', SubmitSupportersSurvey.as_view(), name='submit_supporters_survey'),
]