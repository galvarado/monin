# coding: utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from main.models import Order

class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Número de cliente')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class AccessForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    city = forms.CharField(label='Ciudad')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('client', 'product')

class ClientCreationForm(UserCreationForm):
    pass