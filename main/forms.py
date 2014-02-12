# coding: utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Número de cliente')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class AccessForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    city = forms.CharField(label='Ciudad')