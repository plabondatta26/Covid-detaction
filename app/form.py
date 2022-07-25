from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'password1', 'password2']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CovidUserModel
        fields = '__all__'

