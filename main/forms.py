from django import forms
from django.forms import widgets
from django.forms.widgets import PasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget = forms.PasswordInput)

