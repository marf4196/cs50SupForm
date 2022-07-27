from django.dispatch import receiver
from django.db.models.signals import post_save
from web.models import Students, SupportSurveyHistory

@receiver(post_save, sender=Students)
def save_profile(sender, instance, created, **kwargs):
    if created:
        SupportSurveyHistory.objects.create(student=instance)