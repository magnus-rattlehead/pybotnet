from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Upload

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class CommandAllForm(forms.Form):
    cmdline = forms.CharField(label='Command', max_length=100)
    clients = forms.ModelMultipleChoiceField(
        queryset = Client.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )

class HandleUploadsForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file']
