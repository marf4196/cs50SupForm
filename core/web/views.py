from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

# Create your views here.

def indexView(request):
    return HttpResponse('HEY')

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

class FeedBackPage(TemplateView):
    template_name = 'feed_back.html'

class ClassAttend(View):
    def get(self, request, *args, **kwrags):
        return render(request, 'class_attend_form.html')
    def post(self, request, *args, **kwrags):
        pass
