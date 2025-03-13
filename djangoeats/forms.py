from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User
from djangoeats.models import Review

class ProfileForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES,)

     class Meta:
          model = User
          fields= ['username','email','password'] 


class ReviewForm(forms.ModelForm):
     RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
     rating = forms.ChoiceField(widget=forms.Select,choices=RATING_CHOICES)
     comment = forms.CharField(required=False)

     class Meta:
          model = Review
          fields = ['rating','comment',]

