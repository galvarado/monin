#!/usr/bin/env python
# Este archivo usa el encoding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from main.models import Order, ImageSlider, CategorySample, Category, Product, ProductSample, SiteConfiguration

class AuthForm(AuthenticationForm):
    username = forms.CharField(label=_('Numero de cliente'))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AccessForm(forms.Form):
    name = forms.CharField(label=_('Nombre'))
    email = forms.EmailField(label='Email')
    city = forms.CharField(label=_('Ciudad'))

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('client', 'product')

class CategorySampleCreationForm(forms.ModelForm):
    class Meta:
        model = CategorySample
        exclude = ('active',)

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('active',)

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('active',)

class ProductSampleCreationForm(forms.ModelForm):
    class Meta:
        model = ProductSample
        exclude = ('active',)

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration

class ImageSliderCreationForm(forms.ModelForm):
    class Meta:
        model = ImageSlider
        exclude = ('active',)

class ClientCreationForm(UserCreationForm):
    pass

class ContactFrom(forms.Form):
    name = forms.CharField(label=_('Nombre'))
    email = forms.EmailField(label='Email')
    message = forms.CharField(label=_('Mensaje'), widget=forms.Textarea())

class ConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration

