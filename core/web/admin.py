from django.contrib import admin
from .models import Feedback, ClassAttend, ClassCancel, ClassInfo, NoSupport, Students, SupportSurveyCounter, SupporterSurvey

# Register your models here.
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'ticket', 'created_time', 'updated_time']
    search_fields = ['name', 'email', 'phone', 'ticket']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(Students, StudentsAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'description', 'created_time', 'updated_time']
    search_fields = ['email', 'phone', 'name']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(Feedback, FeedbackAdmin)

class ClassAttendAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'email', 'phone', 'ticket','qr_code','entered', 'canceled', 'created_time', 'updated_time']
    search_fields = ['email', 'phone', 'ticket']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(ClassAttend, ClassAttendAdmin)

class ClassCancelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'ticket','created_time', 'updated_time']
    search_fields = ['email', 'phone']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(ClassCancel, ClassCancelAdmin)

class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ['counter']
admin.site.register(ClassInfo, ClassInfoAdmin)

class NoSupportAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'ticket','created_time', 'updated_time']
    search_fields = ['email', 'phone']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(NoSupport, NoSupportAdmin)

class SupportSurveyCounterAdmin(admin.ModelAdmin):
    list_display = ['student', 'survey_counter', 'created_time', 'updated_time']
    search_fields = ['ticket']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(SupportSurveyCounter, SupportSurveyCounterAdmin)

class SupporterSurveyAdmin(admin.ModelAdmin):
    list_display = ['name', 'token', 'supporter', 'satisfaction', 'validate_status', 'created_time', 'updated_time']
    search_fields = ['name', 'supporter', 'token']
    list_filter = ['validate_status']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(SupporterSurvey, SupporterSurveyAdmin)