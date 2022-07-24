from django.contrib import admin
from django.urls import path
from web.views import (
    WelcomePage, FeedbackView, FindTicketView, 
    ClassAttendView, NoSupportView, test_template, 
    ClassCancelView, StaffLogin)

app_name = 'web'

urlpatterns = [
    path('test/', test_template.as_view(), name='test-template'),
    path('', WelcomePage.as_view(), name='welcome'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('class-cancel/', ClassCancelView.as_view(), name='class-cancel'),
    path('class-attend/', ClassAttendView.as_view(), name='class-attend'),
    path('find-ticket/', FindTicketView.as_view(), name='find-ticket'),
    path('no-support/', NoSupportView.as_view(), name='no-support'),
    path('staff-login/', StaffLogin.as_view(), name='staff-login'),
]