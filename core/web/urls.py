from django.contrib import admin
from django.urls import path
from web.views import WelcomePage, Feedback, FindTicket, ClassAttend, NoSupport, test_template

app_name = 'web'

urlpatterns = [
    path('test/', test_template.as_view(), name='test_template'),
    path('', WelcomePage.as_view(), name='welcome'),
    path('feedback/', Feedback.as_view(), name='feedback'),
    path('class-attend/', ClassAttend.as_view(), name='class-attend'),
    path('find-ticket/', FindTicket.as_view(), name='find-ticket'),
    path('no-support/', NoSupport.as_view(), name='no-support')
]