from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    """
        Registration form for new users
    """

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }
