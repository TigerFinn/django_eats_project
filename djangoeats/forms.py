from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES,)

     class Meta:
          model = User
          fields= ['username','email','password'] 



