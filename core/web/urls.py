from django.urls import path
from web.views import (
    WelcomePage, FeedbackView, FindTicketView, 
    ClassAttendView, NoSupportView, rate_template ,
    ClassCancelView, StaffLogin, StaffLogout, ValidateQRcode)
#from django.conf import settings
#from django.conf.urls.static import static

app_name = 'web'

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome'),
    path('feedback', FeedbackView.as_view(), name='feedback'),
    path('class-cancel', ClassCancelView.as_view(), name='class-cancel'),
    path('class-attend', ClassAttendView.as_view(), name='class-attend'),
    path('find-ticket', FindTicketView.as_view(), name='find-ticket'),
    path('no-support', NoSupportView.as_view(), name='no-support'),
    path('staff-login/', StaffLogin.as_view(), name='staff-login'),
    path('staff-logout', StaffLogout.as_view(), name='staff-logout'),
    path('validate-code/<str:key>/', ValidateQRcode.as_view(), name='validate-code'),  # slug = classAttend.slug
    path('rate', rate_template.as_view(), name='rate-template'),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
#                       static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
