from django.db import models
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
    email = models.EmailField(unique=False, null=False, blank=False)
    phone = models.BigIntegerField(unique=False, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.email}"
    
    class Meta:
        verbose_name = "دانشجو دوره"
        verbose_name_plural = "لیست دانشجویان دوره"


class Feedback(models.Model):
    subject = models.CharField(max_length=256, null= False, blank= False)
    name = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.BigIntegerField(null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "نقد و انتقاد"
        verbose_name_plural = "نقد و انتقادات"

class ClassAttend(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(allow_unicode=True, max_length=255, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.BigIntegerField(null=False, blank=False)
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
        qrcode_image = qrcode.make("https:"+"/"+f"/cs50xiran.com/validate-code/{self.phone}-week5/")
        canvas = Image.new('RGB', (420,420), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        file_name = f'{self.phone}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(file_name, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "شرکت کننده کلاس حضوری"
        verbose_name_plural = "لیست شرکت کنندگان کلاس حضوری"

class ClassCancel(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.BigIntegerField(null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "فرد کنسل کننده کلاس حضوری"
        verbose_name_plural = "لیست کنسل کنندگان کلاس حضوری"


class ClassInfo(models.Model):
    name = models.CharField(max_length=100, default='capacity_counter')
    counter = models.PositiveIntegerField(default=350, validators=[MinValueValidator(0), MaxValueValidator(350)])
    
    def __str__(self):
        return f"{self.name} - {self.counter}"

    class Meta:
        verbose_name = "ظرفیت کلاس حضوری"
        verbose_name_plural = "ظرفیت کلاس حضوری"

class NoSupport(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.BigIntegerField(null=False, blank=False)
    description = models.CharField(max_length=2048, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "فرد بدون پشتیبان"
        verbose_name_plural = "لیست افرادی بدون پشتیبان"

class SupporterSurvey(models.Model):
    user = models.ForeignKey(Students, on_delete=models.DO_NOTHING, blank=False, null=False)
    supporter = models.ForeignKey("TA", on_delete=models.DO_NOTHING, null=False, blank=False)
    satisfaction = models.BooleanField(null=False, blank=False) 
    description = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to="media/TA_evidence/", blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.supporter} - {self.satisfaction}"
    
    class Meta:
        verbose_name = "نظرسنجی TA ها"
        verbose_name_plural = "نظرسنجی TA ها"

class TA(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    discord_id = models.CharField(max_length=255, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.discord_id}"
    
    class Meta:
        verbose_name = "ها TA لیست"
        verbose_name_plural = "ها TA لیست"

