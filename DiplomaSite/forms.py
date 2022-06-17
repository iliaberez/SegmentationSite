from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class SegmentationForm(forms.Form):
    file = forms.FileField(label = 'Add File', widget = forms.FileInput(attrs = {'class':'form-input, file-input'}))
    number_slide = forms.CharField(label = 'Add number slide', widget = forms.NumberInput(attrs = {'class':'form-input'}))
    name_pacient = forms.CharField(label = 'Add name Pacient', widget = forms.TextInput(attrs = {'class':'form-input input-name-pacient'}))
    description = forms.CharField(label = 'Add description', widget= forms.Textarea(attrs= {'class':'form-input input-description'}))
