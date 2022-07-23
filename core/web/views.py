from django.shortcuts import render
from django.views.generic import TemplateView, View

from web.forms import FeedbackForm
from .models import ClassAttend, Feedback, NoSupport, ClassCancel, ClassInfo

# Create your views here.
class test_template(TemplateView):
    template_name = 'feedback_result.html'

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

class ClassAttend(View):
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

class Feedback(View):
    def get(self, request, *args, **kwargs):
        form = FeedbackForm
        context = {'form': form}
        return render(request, 'feedback.html', context)
    
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()    
            context = {'detail': 'نظر شما با موفقیت ثبت شد'}        
            return render(request, 'feedback_result.html', context)
        else:
            context = {'detail': 'متاسفانه ثبت نظر شما با مشکل مواجه شد'} 
            return render(request, 'feedback_result.html', context)
        
class NoSupport(View):
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


