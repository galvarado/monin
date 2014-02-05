# coding: utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "placeholder": "Usuario...",
        "size": "26",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "input",
        "placeholder": "Contraseña...",
        "size": "26",
    }))

class AccessForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    city = forms.CharField(label='Ciudad')