from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = ('username','email')

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = ('username','email')