from django.contrib import admin
from django.urls import path
from web.views import WelcomePage, FeedBack, Classattend, FindTicket, Nosupport

app_name = 'web'

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome'),
    path('feedBack', FeedBack.as_view(), name='feedBack'),
    path('class-attend', Classattend.as_view(), name='classattend'),
    path('find-ticket', FindTicket.as_view(), name='findTicket'),
    path('no-support', Nosupport.as_view(), name='nosupport')
]