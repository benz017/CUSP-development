from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import MinLengthValidator


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Full Name', widget=forms.TextInput(attrs={'class': "form-input", 'id':"name",'placeholder':"Full Name" }))
    username = forms.CharField(max_length=100, help_text='Username', widget=forms.TextInput(attrs={'class': "form-input", 'id':"username",'placeholder':"Username" }))
    email = forms.EmailField(max_length=150, help_text='Email',widget=forms.EmailInput(attrs={'class': "form-input", 'id':"email" ,'placeholder':"Email Address" }))
    password1 = forms.CharField(max_length=16,  validators=[MinLengthValidator(6)], help_text='Password', widget=forms.PasswordInput(attrs={'class': "form-input", 'id':"password" ,'placeholder':"Password" }))
    password2 = forms.CharField(max_length=16, validators=[MinLengthValidator(6)], help_text='Password', widget=forms.PasswordInput(attrs={'class': "form-input", 'id':"re_password" ,'placeholder':"Re-type password" }))
    terms = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "agree-term", 'id':"agree-term"}) )

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2','terms')


class LogInForm(AuthenticationForm):
    username = forms.CharField(max_length=150, help_text='Username', widget=forms.TextInput(attrs={'class': "form-input", 'id':"username",'placeholder':"Username" }))
    password = forms.CharField(max_length=16,  validators=[MinLengthValidator(6)], help_text='Password', widget=forms.PasswordInput(attrs={'class': "form-input", 'id':"password" ,'placeholder':"Password" }))

    class Meta:
        model = User
        fields = ('username', 'password')

