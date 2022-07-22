from email import message
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import ClassAttend

# Create your views here.

def indexView(request):
    return HttpResponse('HEY')

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

class FeedBackPage(TemplateView):
    template_name = 'feed_back.html'

class Classattend(View):
    def get(self, request, *args, **kwrags):
        return render(request, 'class-attend.html')
    def post(self, request, *args, **kwrags):
        name = request.POST['name']
        ticket = request.POST['ticket']
        phone = request.POST['phone']
        email = request.POST['email']

        qs = ClassAttend.objects.filter(ticket = ticket)
        if not qs.exists():
            ClassAttend.objects.create(name = name, email = email, phone = phone, ticket = ticket)
            qs = ClassAttend.objects.get(ticket = ticket)
            # TODO send sms
            context = {}
            context['message'] = 'ثبت نام شما موفق بود'
            context['qrcode'] = qs.qr_code
            return render(request, 'class-attend.html', context)
            
        else:
            qs = ClassAttend.objects.get(ticket = ticket)
            if qs.canceled:
                qs.canceled = False
                qs.save()
                # TODO send sms
                context = {}
                context['message'] = 'ثبت نام شما موفق بود'
                context['qrcode'] = qs.qr_code
                return render(request, 'class-attend.html', context)
            else:
                context = {}
                context['message'] = 'شما ثبت نام کرده بودید :)'
                return render(request, 'class-attend.html', context)

