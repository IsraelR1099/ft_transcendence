from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

import logging
import base64

from .models import Users


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=64, help_text='Required. Add a valid email address')

    class Meta:
        model = Users
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError(
                    "Username must be at least 3 characters long.")
        if not username.isalnum():
            raise forms.ValidationError(
                    "Username must contain only letters and numbers.")
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError(
                    f"Username {username} is already in use.")
        return username


class UsersAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid email or password")


class UsersUpdateForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = (
                'username',
                'email',
                'profile_image',
                )

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = Users.objects.exclude(pk=self.instance.pk)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email is already in use")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        qs = Users.objects.exclude(pk=self.instance.pk)\
            .filter(username=data)
        if qs.exists():
            raise forms.ValidationError("Username is already in use")
        return data

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image', False)
        if profile_image:
            if not profile_image.name.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Image file type is not supported")
        else:
            raise ValidationError("Image file is not valid")
        if profile_image.size > (1024*1024):
            raise ValidationError("Image file size too large (>1MB)")
        return profile_image
