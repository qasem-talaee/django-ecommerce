from django import forms
from captcha.fields import CaptchaField
from django.core.validators import validate_email

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            raise forms.ValidationError('Please insert correct email address')
        return email

class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            raise forms.ValidationError('Please insert correct email address')
        return email

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+-/~'
        if chars in postal_code:
            raise forms.ValidationError('Please enter correct postal code.')
        return postal_code

class LoginStep2Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            raise forms.ValidationError('Please insert correct email address')
        return email

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-0', 'placeholder': 'Search'}))