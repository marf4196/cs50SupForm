from django.contrib import admin
from .models import Messages, PersonRegister

# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_lName', 'student_email', 'student_phone', 'subject', 'support_name', 'created_time', 'updated_time']
    search_fields = ['student_email', 'student_phone', 'support_name']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(Messages, MessagesAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'lName', 'email', 'phone', 'ticket','qr_code', 'created_time', 'updated_time']
    search_fields = ['email', 'phone']
    date_hierarchy = 'created_time'
    ordering = ['-created_time']
admin.site.register(PersonRegister, PersonAdmin)
