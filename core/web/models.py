from django.db import models
from django.forms import DateTimeField
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
# Create your models here.

class Students(models.Model):
    """
        we need to have all the cs50 users data so we can use queries for other end points
    """
    name = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.IntegerField(unique=True, null=False, blank=False)
    ticket = models.CharField(unique=True, max_length=10, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.email}"


class Feedback(models.Model):
    subject = models.CharField(max_length=256, null= False, blank= False)
    name = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

class ClassAttend(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    ticket = models.CharField(max_length=10, blank=False, null=False)
    qr_code = models.ImageField(upload_to='media/qr_codes', blank=True)
    canceled = models.BooleanField(default=False)
    entered = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        # slug config
        if not self.slug:
            self.slug = slugify(f"{self.name}_week4")
        # qr code config
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

class ClassCancel(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.IntegerField(unique=True, null=False, blank=False)
    ticket = models.CharField(unique=True, max_length=10, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

class ClassInfo(models.Model):
    name = models.CharField(max_length=100, default='capacity_counter')
    counter = models.PositiveIntegerField(default=310, validators=[MinValueValidator(0), MaxValueValidator(310)])
    
    def __str__(self):
        return f"{self.name} - {self.counter}"

class NoSupport(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    ticket = models.CharField(max_length=10, blank=False, null=False)
    description = models.CharField(max_length=2048, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)
