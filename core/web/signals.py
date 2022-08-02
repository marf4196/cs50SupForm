# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from web.models import Students, SupportSurveyCounter, SupporterSurvey
# from requests import post

# @receiver(post_save, sender=Students)
# def save_counter(sender, instance, created, **kwargs):
#     if created:
#         SupportSurveyCounter.objects.create(student=instance)

# @receiver(post_save, sender=SupporterSurvey)
# def send_new_score_api(sender, instance, **kwargs):
#     if instance.validate_status:
#         # compute the score
#         score = 0
#         if instance.satisfaction:
#             score += 5
#         else:
#             score -= 5

#         post_data = {
#             "password": "QbwQ77CiYXdlCTg2oLXPuFPZzP2g",
#             "supporter": instance.supporter,
#             "score": score
#         }

#         # send new score
#         # TODO: change url
#         post('https://google.com', json=post_data)

