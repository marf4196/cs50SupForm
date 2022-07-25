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
class test_template(TemplateView):
    template_name = 'download-page.html'

class WelcomePage(TemplateView):
    template_name = 'welcome.html'

class ClassAttendView(View):
    def get(self, request, *args, **kwrags):
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        context = {'capacity': capacity}
        return render(request, 'class-attend.html', context)

    def post(self, request, *args, **kwrags):
        form = ClassAttendForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # we have to check if this user is registered or not
            qs = Students.objects.filter(ticket=ticket, email=email, phone=phone)
            if not qs.exists():
                context = {'detail': 'اطلاعات شما در لیست دانشجویان دوره مبانی ۱۴۰۱ وجود ندارد'} 
                return render(request, 'result.html', context)


            # user who is requesting is not allowed to register if he/she has canceled registration before
            qs = ClassAttend.objects.filter(ticket=ticket, email=email, phone=phone, canceled=False)

            if not qs.exists(): # user must not be allowed to registered more than one time
                
                # if capacity is completed user can not register
                qs = ClassInfo.objects.get(name='capacity_counter')
                if qs.counter < 0:
                    context = {'detail': 'متاسفانه ظرفیت ثبت نام حضوری به پایان رسیده'} 
                    return render(request, 'result.html', context)

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
                context = {
                    'detail': 'شما قبلا برای حضور در این جلسه ثبت نام کردید، میتوانید از لینک زیر بلیط خود را دریافت کنید',
                    'link': f"/{qs[0].qr_code}",
                    'ticket': qs[0].ticket,
                }
                return render(request, 'download-ticket.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد'} 
            return render(request, 'result.html', context)


class ClassCancelView(View):
    def get(self, request, *args, **kwargs):
        capacity = ClassInfo.objects.get(name='capacity_counter').counter
        context = {'capacity': capacity}
        return render(request, 'class-cancel.html', context)

    def post(self, request, *args, **kwargs):
        form = ClassCancelForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # user registration info must be found it CLassAttend
            qs = ClassAttend.objects.filter(ticket=ticket, email=email, phone=phone, canceled=False)
            if not qs.exists():
                context = {'detail': 'اطلاعات شما در لیست ثبت نام حضوری وجود ندارد'} 
                return render(request, 'result.html', context)
            
            qs[0].canceled = True
            qs[0].save()
            form.save()

            # increase capacity
            qs = ClassInfo.objects.get(name='capacity_counter')
            qs.counter += 1
            qs.save()

            # TODO: Send SMS

            context = {'detail': 'انصراف شما از حضور در جلسه با موفقیت ثبت شد'} 
            return render(request, 'result.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد'} 
            return render(request, 'result.html', context)


class FindTicketView(View):
    def get(self, request, *args, **kwargs):
        form = TicketForm
        context = {'form': form}
        return render(request, 'find-ticket.html', context)

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data.get('ticket')
            qs = ClassAttend.objects.filter(ticket=ticket)
            if qs.exists():
                qs = ClassAttend.objects.get(ticket=ticket)
                if qs.canceled:
                    context = {'detail': 'ثبت نام حضوری شما لغو شده و امکان دریافت بلیط را ندارید'} 
                    return render(request, 'result.html', context)
                else:
                    context = {
                            'detail': 'در صورتی که فایل بلیط شما دانلود نشده است بر روی دکمه زیر کلیک کنید',
                            'link': f"/{qs.qr_code}",
                            'ticket': qs.ticket
                        }
                    return render(request, 'download-ticket.html', context)
            else: # qs doesn't exist
                context = {'detail': 'شما برای جلسه حضوری ثبت نام نکرده اید'} 
                return render(request, 'result.html', context)
        else: # form is not valid
            context = {'detail': 'ورودی ارسالی قابل قبول نمی باشد'} 
            return render(request, 'result.html', context)

class FeedbackView(View):
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
            user = Students.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
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
        
class NoSupportView(View):
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
            user = Students.objects.get(Q(phone=phone) | Q(ticket=ticket) | Q(email=email))
            
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
                return render(request, 'result.html', context)
            else:
                context = {'detail': 'نام کاربری یا رمز عبور اشتباه است'} 
                return render(request, 'result.html', context)

        else: # form is not valid
            context = {'detail': 'ورودی های ارسالی قابل قبول نمی باشد'} 
            return render(request, 'result.html', context)

class StaffLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/staff-login/')

class ValidateQRcode(View, LoginRequiredMixin):
    def get(self, slug, request, *args, **kwargs):
        # TODO: manage QRcode
        pass
