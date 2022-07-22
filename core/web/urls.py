from django.contrib import admin
from django.urls import path
from web.views import WelcomePage

app_name = 'web'

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome'),
]