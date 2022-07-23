from email import message
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import ClassAttend, Feedback, NoSupport, ClassCancel, ClassInfo

# Create your views here.

def indexView(request):
    return HttpResponse('HEY')

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

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
            context['ticket'] = qs.ticket
            return render(request, 'find-ticket.html', context)
            
        else:
            qs = ClassAttend.objects.get(ticket = ticket)
            if qs.canceled:
                qs.canceled = False
                qs.save()
                # TODO send sms
                context = {}
                context['message'] = 'ثبت نام شما موفق بود'
                context['qrcode'] = qs.qr_code
                context['ticket'] = qs.ticket
                return render(request, 'find-ticket.html', context)
            else:
                context = {}
                context['message'] = 'شما ثبت نام کرده بودید :)'
                return render(request, 'class-attend.html', context)

class FindTicket(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'find-ticket.html')
    def post(self, request, *args, **kwargs):
        ticket = request.POST['ticket']
        qs = ClassAttend.objects.filter(ticket = ticket)
        if qs.exists():
            qs = ClassAttend.objects.get(ticket = ticket)
            if qs.canceled:
                print('shoma sabt nametoon ro ghablan cancel kardid')
            else:
                context = {}
                context['qrcode'] = qs.qr_code
                return render(request, 'download-page.html', context)

        else:
            print('sabt nam nakardi')

class FeedBack(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'feed-back.html')
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']

        Feedback.objects.create(name = name, phone = phone, email = email, subject = subject, description = description)

        context = {}
        context['message'] = 'ممنون بابت انتقاد/پیشنهادتون \n اطلاعات شما دریافت شد'
        return render(request, 'feed-back.html', context)

class Nosupport(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'no-support.html')
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        ticket = request.POST['ticket']

        NoSupport.objects.create(name = name, phone = phone, email = email, ticket = ticket)

        context = {}
        context['message'] = 'اصطلاعات شما ثبت شد و تا ۲۴ ساعت با شما تماس گرفته خواهد شد'
        
        return render(request, 'no-support.html', context)

# class ClassCancel(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'class-cancel.html')
#     def post(self, request, *args, **kwargs):
#         phone = request.POST['phone']
#         email = request.POST['email']
#         ticket = request.POST['ticket']


