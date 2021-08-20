from django.db.models import fields
from onlineshop.models import Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from . models import *


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}))
    

    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}))

    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}),
        'first_name':forms.TextInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}),
        'last_name':forms.TextInput(attrs={'class':'appearance-none border rounded w-full py-2 px-3 text-grey-darker'}),
        }


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        exclude = ('id',)
        widgets = {'user': forms.HiddenInput()}
class CustomeruserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']
