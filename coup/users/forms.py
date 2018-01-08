from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, getChoices

import urllib.request
# import urllib.parse


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    faculty = forms.ChoiceField(
        required=False,
        choices = User.FACULTY_CHOICES
    )
    program = forms.ChoiceField(
        required=False,
        choices = getChoices()
    )
    bio = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
                    'first_name',
                    'last_name',
                    'email',
                    'faculty',
                    'program',
                    'bio'
                )
