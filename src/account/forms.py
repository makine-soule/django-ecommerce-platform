from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

        widgets = {
            "username":forms.TextInput(attrs={"placeholder":"Enter your username . . ."}),
            "email": forms.TextInput(attrs={"placeholder": "Enter your email . . ."}),
            "first_name": forms.TextInput(attrs={"placeholder": "Enter your first_name . . ."}),
            "last_name": forms.TextInput(attrs={"placeholder": "Enter your last_name . . ."})
        }

class UpdateUserForm(forms.ModelForm):
    password = None
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]
        exclude = [
            "password1",
            "password2",
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'required': 'required'}),
        }