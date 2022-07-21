from django.contrib import admin
from django.urls import path
from .views import indexView

app_name = 'web'

urlpatterns = [
    path('', indexView, name='index'),
]