from django.db import models
from django.forms import DateTimeField
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

class Messages(models.Model):
    subject = models.CharField(max_length=256, null= False, blank= False)
    student_name = models.CharField(max_length=256, blank=False, null=False)
    student_lName = models.CharField(max_length=256, blank=False, null=False)
    student_email = models.EmailField(null=False, blank=False)
    student_phone = models.IntegerField(null=False, blank=False)
    support_name = models.CharField(max_length=512, blank=False, null=False)
    description = models.CharField(max_length=2048, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.student_phone

class PersonRegister(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    lName = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    ticket = models.CharField(max_length=10, blank=False, null=False)
    qr_code = models.ImageField(upload_to='media/qr_codes', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.phone)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(self.ticket)
        canvas = Image.new('RGB', (290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        file_name = f'{self.ticket}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(file_name, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)