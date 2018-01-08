from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from ..users.models import User, getChoices

class SignUpForm (UserCreationForm):
    """
    This form extends from the basic UserCreationForm,
    which is responsible for USERNAME and PASSWORD fields.
    """
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'User Name'}),required = True)
    email = forms.EmailField(label='E-mail Address', widget=forms.TextInput(attrs={'placeholder': 'E-mail Address'}),required = True)
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),required = True)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),required = True)

    class Meta:
        model = User
        # order of field appearance
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
