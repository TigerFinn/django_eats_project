from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User
from djangoeats.models import Review

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

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
     rating = forms.ChoiceField(widget=forms.Select,choices=RATING_CHOICES)
     comment = forms.CharField(required=False)

     class Meta:
          model = Review
          fields = ['rating','comment',]

class SearchForm(forms.ModelForm):
     name = forms.CharField(required=False)
     location = forms.CharField(required=False)
     cuisine = forms.CharField(required=False)
     rating = forms.ChoiceField(widget = forms.Select, choices=RATING_CHOICES)

     class Meta:
          fields = ['name','location','cuisine','rating']

