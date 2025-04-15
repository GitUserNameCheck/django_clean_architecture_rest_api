from django import forms
from django.forms import FloatField, ModelForm, TextInput, ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from clean_architecture.modules.infrastructure.db import Service


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {            
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),          
            'password1': forms.PasswordInput(attrs={"class": "form-control"}),      
            'password2': forms.PasswordInput(attrs={"class": "form-control"}),          
        }

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class NumberInput(TextInput):
    input_type = 'number'

class ServicePriceForm(ModelForm):
    price = FloatField(
        required=True,
        widget=NumberInput(attrs={'min': '0', 'step': '0.01'})
    )

    class Meta:
        model = Service
        fields = ['price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["price"] = self.initial["price"] / 100

    def clean_price(self):
        price = self.cleaned_data['price']

        if price < 0:
            raise ValidationError("Price cannot be negative.")

        return int(price * 100)
