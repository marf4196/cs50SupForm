from django.urls import path
from web.views import (
    WelcomePage, FeedbackView, FindTicketView, 
    ClassAttendView, NoSupportView, rate_template ,
    ClassCancelView, StaffLogin, StaffLogout, ValidateQRcode)

app_name = 'web'

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome'),
    path('123feedback', FeedbackView.as_view(), name='feedback'),
    path('123class-cancel', ClassCancelView.as_view(), name='class-cancel'),
    path('class-attend-test', ClassAttendView.as_view(), name='class-attend'),
    path('123find-ticket', FindTicketView.as_view(), name='find-ticket'),
    path('123no-support', NoSupportView.as_view(), name='no-support'),
    path('staff-login/', StaffLogin.as_view(), name='staff-login'),
    path('staff-logout', StaffLogout.as_view(), name='staff-logout'),
    path('123validate-code/<slug:slug>/', ValidateQRcode.as_view(), name='validate-code'),  # slug = classAttend.slug
    path('123rate', rate_template.as_view(), name='rate-template'),
]
