from django import forms
from web.models import Feedback, NoSupport

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "name", "email", "phone", "description"]

class NoSupport(forms.ModelForm):
    class Meta:
        model = NoSupport
        fields = ["name", "email", "phone", "ticket", "description"]