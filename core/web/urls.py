from django.contrib import admin
from django.urls import path
from web.views import WelcomePage, FeedBackPage, Classattend

app_name = 'web'

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome'),
    path('feedBack', FeedBackPage.as_view(), name='feedBack'),
    path('class-attend', Classattend.as_view(), name='classattend'),
]