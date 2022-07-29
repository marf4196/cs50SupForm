from django import forms
from web.models import Feedback, NoSupport, ClassAttend, ClassCancel, SupporterSurvey

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "name", "email", "phone", "description"]

class NoSupportForm(forms.ModelForm):
    class Meta:
        model = NoSupport
        fields = ["name", "email", "phone", "ticket"]

class TicketForm(forms.Form):
    ticket = forms.CharField(max_length=6, required=True)

class ClassAttendForm(forms.ModelForm):
    class Meta:
        model = ClassAttend
        fields = ['name', 'email', 'phone', 'ticket']

class ClassCancelForm(forms.ModelForm):
    class Meta:
        model = ClassCancel
        fields = ['name', 'email', 'phone', 'ticket']

class StaffLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
