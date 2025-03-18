from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User
from djangoeats.models import Review

class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())

     class Meta:
          model = User
          fields= ['username','email','password'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type']


class ReviewForm(forms.ModelForm):
     RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
     rating = forms.ChoiceField(widget=forms.Select,choices=RATING_CHOICES)
     comment = forms.CharField(required=False)

     class Meta:
          model = Review
          fields = ['rating','comment',]


class RegisterForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput)

     class Meta:
          model = User
          fields = ['username', 'email', 'password']