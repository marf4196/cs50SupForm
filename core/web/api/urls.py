from django.urls import path
from .views import SupportSurvey

urlpatterns = [
    path('submit_TA_survey/', SupportSurvey.as_view(), name='submit_TA_survey'),
]