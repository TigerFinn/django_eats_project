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
     name = forms.CharField(max_length=Restaurant.NAME_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter the name of your restaurant'}),help_text='name')
     cuisine = forms.CharField(max_length=Restaurant.CUISINE_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s cuisine'}),help_text='cuisine')
     address = forms.CharField(max_length=Restaurant.ADDRESS_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s address'}),help_text='address')
     email = forms.EmailInput()
     phone = forms.CharField(max_length=Restaurant.PHONE_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s phone number'}),help_text='phone')
     image = forms.ImageField(required=False, help_text="Upload an image for your restaurant")
     slug = forms.CharField(widget=forms.HiddenInput(), required=False)

     class Meta:
          model = Restaurant
          exclude = ['slug','owner',]

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description']

