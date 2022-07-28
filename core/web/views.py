from multiprocessing import context
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from web.forms import (
    FeedbackForm, NoSupportForm, TicketForm, 
    ClassAttendForm, ClassCancelForm, StaffLoginForm)
from web.models import ClassAttend, NoSupport, ClassInfo, Students
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class rate_template(TemplateView):
    template_name = 'rate.html'

class WelcomePage(TemplateView):
    template_name = 'index.html'

class ClassAttendView(View):
    def get(self, request, *args, **kwrags):
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        context = {'capacity': capacity}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwrags):
        form = ClassAttendForm(request.POST)
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # we have to check if this user is registered or not
            qs = Students.objects.filter(ticket=ticket, email=email, phone=phone)
            if not qs.exists():
                context = {'detail': 'اطلاعات شما در لیست دانشجویان دوره مبانی ۱۴۰۱ وجود ندارد', 'capacity': capacity}
                return render(request, 'register.html', context)


            # user who is requesting is not allowed to register if he/she has canceled registration before
            # there was a bug if canceled is true was in qs, user can register again but when a user with 2 registraion
            # 1 canceled and 1 is not canceled want to download ticket it will raise an error:
            # get() returned more than one ClassAttend -- it returned 2!
            qs = ClassAttend.objects.filter(ticket=ticket, email=email, phone=phone)

            if not qs.exists(): # user must not be allowed to registered more than one time
                
                # if capacity is completed user can not register
                qs = ClassInfo.objects.get(name='capacity_counter')
                if qs.counter < 0:
                    context = {'detail': 'متاسفانه ظرفیت ثبت نام حضوری به پایان رسیده', 'capacity': capacity}
                    return render(request, 'register.html', context)

                # decrease capacity
                qs.counter -= 1
                qs.save()

                # TODO send sms

                user = form.save()
                context = {
                    'detail': 'ثبت نام شما با موفقیت انجام شد، در صورتی که بلیط شما به صورت خودکار دانلود نشد، از دکمه دانلود استفاده کنید',
                    'link': f"/{user.qr_code}",
                    'ticket': user.ticket,
                }
                return render(request, 'download-ticket.html', context)
                
            else: # user has registered already
                qs = ClassAttend.objects.get(ticket = ticket)
                # user registered but has attribiute canceled = true so we make it false
                if qs.canceled:
                    qs.canceled = False
                    context = {
                    'detail': 'ثبت نام شما با موفقیت انجام شد، در صورتی که بلیط شما به صورت خودکار دانلود نشد، از دکمه دانلود استفاده کنید',
                    'link': f"/{qs.qr_code}",
                    'ticket': qs.ticket,
                    }
                    return render(request, 'download-ticket.html', context)
                # user registered with attribiute canceled = false
                else:
                    context = {
                        'detail': 'شما قبلا برای حضور در این جلسه ثبت نام کردید، میتوانید از لینک زیر بلیط خود را دریافت کنید',
                        'link': f"/{qs.qr_code}",
                        'ticket': qs.ticket,
                    }
                    return render(request, 'download-ticket.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد'} 
            return render(request, 'report.html', context)


class ClassCancelView(View):
    def get(self, request, *args, **kwargs):
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        context = {'capacity': capacity}
        return render(request, 'deregister.html', context)

    def post(self, request, *args, **kwargs):
        form = ClassCancelForm(request.POST)
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # user registration info must be found it CLassAttend
            qs = ClassAttend.objects.filter(ticket=ticket, email=email, phone=phone, canceled=False)
            if not qs.exists():
                context = {'detail': 'اطلاعات شما در لیست ثبت نام حضوری وجود ندارد', 'capacity': capacity}
                return render(request, 'deregister.html', context)
            
            qs = ClassAttend.objects.get(ticket=ticket)
            qs.canceled = True
            qs.save()
            form.save()

            # increase capacity
            qs = ClassInfo.objects.get(name='capacity_counter')
            qs.counter += 1
            qs.save()

            # TODO: Send SMS

            context = {'detail': 'انصراف شما از حضور در جلسه با موفقیت ثبت شد', 'capacity': capacity}
            return render(request, 'deregister.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد', 'capacity': capacity}
            return render(request, 'deregister.html', context)


class FindTicketView(View):
    def get(self, request, *args, **kwargs):
        form = TicketForm
        context = {'form': form}
        return render(request, 'lost.html', context)

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            qs = ClassAttend.objects.filter(ticket=ticket)
            if qs.exists():
                qs = ClassAttend.objects.get(ticket=ticket)
                if qs.canceled:
                    context = {'detail': 'ثبت نام حضوری شما لغو شده و امکان دریافت بلیط را ندارید'} 
                    return render(request, 'lost.html', context)
                else:
                    context = {
                            'detail': 'در صورتی که فایل بلیط شما دانلود نشده است بر روی دکمه زیر کلیک کنید',
                            'link': f"/{qs.qr_code}",
                            'ticket': qs.ticket
                        }
                    return render(request, 'download-ticket.html', context)
            else: # qs doesn't exist
                context = {'detail': 'شما برای جلسه حضوری ثبت نام نکرده اید'} 
                return render(request, 'lost.html', context)
        else: # form is not valid
            context = {'detail': 'ورودی ارسالی قابل قبول نمی باشد'} 
            return render(request, 'lost.html', context)

class FeedbackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedbackForm
        context = {'form': form}
        return render(request, 'report.html', context)
    
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            """is this user registered in course?"""
            phone = form.cleaned_data.get('phone')
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            
            # it's possible that user enter one of the above fields incorrectly so we must use query with or condition 
            user = Students.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
            if user is not None: # TODO if none of the phone ticket email is valid it will return an error    
                form.save()    
                context = {'detail': 'نظر شما با موفقیت ثبت شد'}        
                return render(request, 'report.html', context)
            
            else: # form is valid but user is not registered
                context = {'detail': 'متاسفانه ثبت نظر شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
                return render(request, 'report.html', context)
       
        else:
            context = {'detail': 'متاسفانه ثبت نظر شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
            return render(request, 'report.html', context)
        
class NoSupportView(View):
    def get(self, request, *args, **kwargs):
        form = NoSupportForm(request.POST)
        context = {'form': form}
        return render(request, 'support.html', context)
    
    def post(self, request, *args, **kwargs):
        form = NoSupport(request.POST)
        if form.is_valid():
            """is this user registered in course?"""
            phone = form.cleaned_data.get('phone')
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            
            # it's possible that user enter one of the above fields incorrectly so we must use query with or condition 
            user = Students.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
            if user is not None: #TODO if none of the phone ticket email is valid it will return an error    
                form.save()    
                context = {'detail': 'اطلاعات شما ثبت و تا ۲۴ ساعت آینده با شما ارتباط گرفته خواهد شد'}        
                return render(request, 'support.html', context)
            
            else: # form is valid but user is not registered
                context = {'detail': 'متاسفانه ثبت درخواست شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
                return render(request, 'support.html', context)
       
        else:
            context = {'detail': 'متاسفانه ثبت درخواست شما با مشکل مواجه شد، ممکن است شما اطلاعات فرم را بدرستی وارد نکرده و یا از دانشجو های دوره نباشید'} 
            return render(request, 'support.html', context)
        
class StaffLogin(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['detail'] = 'شما قبلا وارد شدید'
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                context = {'detail': 'با موفقیت وارد شدید'} 
                return render(request, 'report.html', context)
            else:
                context = {'detail': 'نام کاربری یا رمز عبور اشتباه است'} 
                return render(request, 'report.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد'} 
            return render(request, 'report.html', context)

class StaffLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/staff-login/')

class ValidateQRcode(View, LoginRequiredMixin):
    def get(self, request, slug, **kwargs): # you cant take slug and *args
        if request.user.is_authenticated: # only staff can view this
            ticket = slug[0:6]
            qs = ClassAttend.objects.filter(ticket = ticket)
            if qs.exists():
                qs = ClassAttend.objects.get(ticket = ticket)
                if qs.canceled: # checks if user has canceled his registration
                    context = {'detail': 'ثبت نام قبلا کنسل شده'}
                    context['ok'] = 0
                    return render(request, 'report.html', context)
                if qs.entered: # checks if user has entered
                    context = {'detail': 'قبلا وارد شده'}
                    context['ok'] = 0
                    return render(request, 'report.html', context)
                # if none of above condition is true so student can enter the class
                qs.entered = True
                qs.save()
                context = {'detail': 'میتواند وارد شود'}
                context['ok'] = 1
                return render(request, 'report.html', context)

            else: # cant find user with that qrcode (it will happen only if they edit url)
                context = {'detail': 'برای کلاس حضوری ثبت نام نشده'}
                return render(request, 'report.html', context)
        else:
            return redirect('/staff-login/')