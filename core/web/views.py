from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def indexView(request):
    return HttpResponse('HEY')

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

class FeedBackPage(TemplateView):
    template_name = 'feed_back.html'