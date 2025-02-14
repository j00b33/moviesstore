from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    security_question = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Security Question'}))
    security_answer = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Security Answer'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter your username',
            'password1': 'Enter a strong password',
            'password2': 'Confirm your password',
            'security_question': 'Enter your security question',
            'security_answer': 'Enter the answer to your security question',
        }
        for fieldname in ['username', 'password1', 'password2', 'security_question', 'security_answer']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control', 'placeholder': placeholders[fieldname]})
            

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}), required=True)
    security_answer = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Answer to Security Question'}))
