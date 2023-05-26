import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# form used to register a new user
class UserRegisterForm(UserCreationForm):
    # fields of UserCreationForm
    email = forms.EmailField(required=True)

    # class with nested namespace for configurations
    class Meta:
        # model interact with form
        model = User
        # field which display in form in order
        fields = ['username', 'email', 'password1', 'password2']
        # text displayed below the form to help the user enter the correct characters
        help_texts = {
            'username': 'Required. 20 characters or fewer. Language special characters allowed, digits and @/./+/-/_ only. The spaces at the front and back of the user name will be removed.'
        }

    # method that raising a validation error if user want to register email which already exist in users table
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("The given email is already registered")
        return self.cleaned_data['email']


# form used to update user information from the profile page
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': 'Required. 20 characters or fewer. Language special characters allowed, digits and @/./+/-/_ only. The spaces at the front and back of the user name will be removed.'
        }

    # method that raising a validation error if user provide invalid characters
    def clean_username(self):
        username = self.cleaned_data['username']
        regex = r'^[\w.@+-]+\Z'
        if not re.search(regex, username):
            raise forms.ValidationError('Provide a valid username')
        return self.cleaned_data['username']
