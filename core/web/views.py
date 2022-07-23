from django.shortcuts import render
from django.views.generic import TemplateView, View
from web.forms import FeedbackForm, NoSupportForm, TicketForm
from .models import ClassAttend, Feedback, NoSupport, ClassCancel, ClassInfo
from django.db.models import Q
from web.models import User
# Create your views here.
class test_template(TemplateView):
    template_name = 'class-cancel.html'

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

class ClassCancel(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'class-cancel.html')

    def post(self, request, *args, **kwargs):
        pass        

class FindTicket(View):
    def get(self, request, *args, **kwargs):
        form = TicketForm
        context = {'form': form}
        return render(request, 'find-ticket.html', context)

    def post(self, request, *args, **kwargs):
        ticket = request.POST['ticket']
        qs = ClassAttend.objects.filter(ticket=ticket)
        if qs.exists():
            qs = ClassAttend.objects.get(ticket=ticket)
            if qs.canceled:
                context = {'detail': 'ثبت نام حضوری شما با موفقیت لغو شد'} 
                return render(request, 'result.html', context)
            else:
                context = {'detail': 'متاسفانه لغو ثبت نام شما موفقیت آمیز نبود'} 
                return render(request, 'result.html', context)

        else:
            context = {'detail': 'شما برای جلسه حضوری ثبت نام نکرده بوده اید'} 
            return render(request, 'result.html', context)

class Feedback(View):
    def get(self, request, *args, **kwargs):
        form = FeedbackForm
        context = {'form': form}
        return render(request, 'feedback.html', context)
    
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            """is this user registered in course?"""
            phone = form.cleaned_data.get('phone')
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            
            # it's possible that user enter one of the above fields incorrectly so we must use query with or condition 
            user = User.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
            if user is not None:    
                form.save()    
                context = {'detail': 'نظر شما با موفقیت ثبت شد'}        
                return render(request, 'result.html', context)
            
            else: # form is valid but user is not registered
                context = {'detail': 'متاسفانه ثبت نظر شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
                return render(request, 'result.html', context)
       
        else:
            context = {'detail': 'متاسفانه ثبت نظر شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
            return render(request, 'result.html', context)
        
class NoSupport(View):
    def get(self, request, *args, **kwargs):
        form = NoSupportForm
        context = {'form': form}
        return render(request, 'no-support.html', context)
    
    def post(self, request, *args, **kwargs):
        form = NoSupport(request.POST)
        if form.is_valid():
            """is this user registered in course?"""
            phone = form.cleaned_data.get('phone')
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            
            # it's possible that user enter one of the above fields incorrectly so we must use query with or condition 
            user = User.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
            if user is not None:    
                form.save()    
                context = {'detail': 'اطلاعات شما ثبت و تا ۲۴ ساعت آینده با شما ارتباط گرفته خواهد شد'}        
                return render(request, 'result.html', context)
            
            else: # form is valid but user is not registered
                context = {'detail': 'متاسفانه ثبت درخواست شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
                return render(request, 'result.html', context)
       
        else:
            context = {'detail': 'متاسفانه ثبت درخواست شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
            return render(request, 'result.html', context)
        


