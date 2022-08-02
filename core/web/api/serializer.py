from rest_framework import serializers
from web.models import SupporterSurvey, Students

class SupportSurveySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.IntegerField()
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = SupporterSurvey
        read_only_fields = ['name', 'phone', 'email']
        fields = ['name', 'phone', 'email', 'supporter', 'satisfaction', 'description', 'image_url']

    def validate(self, attrs):
        name = attrs.pop('name')
        phone = attrs.pop('phone')
        email = attrs.pop('email')
        supporter = attrs.get('supporter')
        if name is None:
            raise serializers.ValidationError('نام وارد نشده است')
        if phone is None:
            raise serializers.ValidationError('شماره تلفن وارد نشده است')
        if email is None:
            raise serializers.ValidationError('ایمیل وارد نشده است')
        if supporter is None:
            raise serializers.ValidationError('پشتیبانی انتخاب نشده است')
        
        # if user has not submitted survey about this supporter before, we have to allow him/her to submit
        try:
            SupporterSurvey.objects.get(user__email=email, user__phone=phone, supporter=supporter)
            raise serializers.ValidationError('شما قبلا برای این TA ثبت نظر کردید')

        except SupporterSurvey.DoesNotExist:
            # user has not submitted survey about this supporter, so everything is fine
            user = Students.objects.filter(email=email, phone=phone)
            
            # user must be registered into the course
            if not user.exists():
                raise serializers.ValidationError('اطلاعات شما در لیست ثبت نامی های دوره مبانی ۱۴۰۱ یافت نشد')
            
            attrs['user'] = user[0]
        return super().validate(attrs)
