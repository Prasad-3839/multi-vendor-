from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def clean_username(self):
        username=self.cleaned_data.get('username')

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if "@" not in email:
            raise forms.ValidationError("Enter a valid email address")

        return email