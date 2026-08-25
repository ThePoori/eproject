from django import forms
from django.utils import choices
from blog.models import Ticket


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد','پیشنهاد'),
        ('گزارش','گزارش'),
        ('انتقاد','انتقاد'),
    )
    message = forms.CharField(widget = forms.Textarea, required = True, label = 'متن')
    name = forms.CharField(max_length = 250, required = True, label = 'نام')
    email = forms.EmailField(label = 'ایمیل')
    phone = forms.CharField(max_length = 11, required = True, label = 'شماره همراه')
    subject = forms.ChoiceField(required = True, choices = SUBJECT_CHOICES, label = 'موضوع')
    