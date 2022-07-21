from django.db import models
from django.forms import DateTimeField

# Create your models here.

class Messages(models.Model):
    SUBJECT_TYPES = (
        ('عدم ارتباط پشتیبان', 'عدم ارتباط پشتیبان'),
        ('عدرم رضایت از پشتیبان', 'عدم رضایت از پشتیبان'),
        ('انتقاد یا پیشنهاد', 'انتقاد یا پیشنهاد'),
    )
    subject = models.CharField(max_length=256, choices=SUBJECT_TYPES)
    student_name = models.CharField(max_length=256, blank=False, null=False)
    student_lName = models.CharField(max_length=256, blank=False, null=False)
    student_email = models.EmailField(null=False, blank=False)
    student_phone = models.IntegerField(null=False, blank=False)
    support_name = models.CharField(max_length=512, blank=False, null=False)
    description = models.CharField(max_length=2048, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)