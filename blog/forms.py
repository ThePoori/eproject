from django import forms
from django.utils import choices
from blog.models import *


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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError("شماره موبایل عددی نیست")
        else:
            return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است")
            else:
                return name
    class Meta:
        model = Comment
        fields = ['name', 'body']
