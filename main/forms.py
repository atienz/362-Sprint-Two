from django import forms
from .models import MyModel
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Profile Form
class MyForm(forms.ModelForm):
    # Defines form attributes
    class Meta:
        model = MyModel
        fields = ["first_name", "middle_name", "last_name", "age", ]
        # Customizes form field labels to display
        labels = {'first_name': "Name", 'middle_name': "Middle", 'last_name': "Last", 'age': "Age", }


# Register Form
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


# User List Form


# UI Home
