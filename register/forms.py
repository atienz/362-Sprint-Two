from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def clean_user(self):
        username = self.cleaned_data.get("username") 
        for instance in User.objects.all():
            if instance.username == username:
                raise forms.ValidationError()
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email") 
        for instance in User.objects.all():
            if instance.email == email:
                raise forms.ValidationError('Email is already in use')
        return email
