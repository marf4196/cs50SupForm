from django.urls import path
from .views import CheckToken

urlpatterns = [
    path('check_token/', CheckToken.as_view(), name='check_token')
]