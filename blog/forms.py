from django import forms
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


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول")
    image2 = forms.ImageField(label="تصویر دوم")
    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 2:
                raise forms.ValidationError("عنوان باید طول رشته بیشتری داشته باشد.")
            else:
                return title
    def clean_description(self):
        description = self.cleaned_data['description']
        if description:
            if len(description) >= 250:
                raise forms.ValidationError("مقدار متن توضیحات زیاد میباشد.")
            else:
                return description
    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']


class SearchForm(forms.Form):
    query = forms.CharField()


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length = 250, required = True)
#     password = forms.CharField(max_length = 250, required = True, widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput, label = 'password')
    password2 = forms.CharField(max_length = 20, widget = forms.PasswordInput, label = 'repeat password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name' , 'email']

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']