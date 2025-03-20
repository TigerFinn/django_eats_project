from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User
from djangoeats.models import Review
from djangoeats.models import Restaurant
from djangoeats.models import MenuItem

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

class RestaurantForm(forms.ModelForm):
     owner = forms.CharField(max_length=50,help_text="Please enter the owner of the Restaurant")
     name = forms.CharField(max_length=Restaurant.NAME_MAX_LENGTH,help_text="Please enter the name of your Restaurant")
     cuisine = forms.CharField(max_length=Restaurant.CUISINE_MAX_LENGTH,help_text="Please enter your restaurants Cuisine")
     address = forms.CharField(max_length=Restaurant.ADDRESS_MAX_LENGTH,help_text="Please enter the Address of your Restaurant")
     email = forms.EmailInput()
     phone = forms.CharField(max_length=Restaurant.PHONE_MAX_LENGTH,help_text="Please enter your restaurants phone number")
     image = forms.ImageField(required=False, help_text="Upload an image for your restaurant")
     slug = forms.CharField(widget=forms.HiddenInput(), required=False)

     class Meta:
          Model = Restaurant
          exclude = ['slug',]

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description']

