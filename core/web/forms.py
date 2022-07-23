from django import forms
from web.models import Feedback, NoSupport

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "name", "email", "phone", "description"]

class NoSupportForm(forms.ModelForm):
    class Meta:
        model = NoSupport
        fields = ["name", "email", "phone", "ticket", "description"]

class TicketForm(forms.Form):
    ticket = forms.CharField(max_length=6, required=True)