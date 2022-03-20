from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _ 
from . models import Student

class StudentRegForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email',  'session',
        'student_id', 'dept', 'home_town', 'profile_image', 'hall']

        labels = {'username': 'Full Name',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Institute Email',
                  'dept': 'Department Name',
                  'session': 'Session',
                  'student_id': 'Student ID',
                  'home_town': 'Hometown',
                  'profile_image': 'Profile Image',
                  'hall': 'Attached Hall'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'home_town': forms.TextInput(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget= forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

