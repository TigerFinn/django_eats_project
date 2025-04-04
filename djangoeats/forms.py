from django import forms
from djangoeats.models import Profile
from django.contrib.auth.models import User
from djangoeats.models import Review
from djangoeats.models import Restaurant
from djangoeats.models import MenuItem

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

#It's a user form
class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
    
     class Meta:
          model = User
          fields= ['username','email','password'] 

#Profile form that works beyond the user form to provide specific functionality for our two types of user and location search
class ProfileForm(forms.ModelForm):
    latitude = forms.DecimalField(required=True, widget=forms.HiddenInput())
    longitude = forms.DecimalField(required=True, widget=forms.HiddenInput(),error_messages={'required':'Please choose a location so you can search for nearby!'})
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta:
        model = Profile
        fields = ['user_type', 'latitude', 'longitude']


#Form for reviewing restaurants
class ReviewForm(forms.ModelForm):
     rating = forms.ChoiceField(
          widget=forms.Select(attrs={
               'class': 'form-select',
               'style': 'max-width: 120px'
          }),
          choices=RATING_CHOICES)
     comment = forms.CharField(
          required=False,
          widget=forms.Textarea(attrs={
               'class': 'form-textarea',
               'placeholder': 'Leave a comment',
               'rows': 4
          }))

     class Meta:
          model = Review
          fields = ['rating','comment',]

# #RIP the search form, we never used it
# class SearchForm(forms.ModelForm):
#      name = forms.CharField(required=False)
#      location = forms.CharField(required=False)
#      cuisine = forms.CharField(required=False)
#      rating = forms.ChoiceField(widget = forms.Select, choices=RATING_CHOICES)

#      class Meta:
#           fields = ['name','location','cuisine','rating']

#A form for restaurants
class RestaurantForm(forms.ModelForm):
     name = forms.CharField(max_length=Restaurant.NAME_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter the name of your restaurant'}),help_text='name')
     cuisine = forms.CharField(max_length=Restaurant.CUISINE_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s cuisine'}),help_text='cuisine')
     address = forms.CharField(max_length=Restaurant.ADDRESS_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s address'}),help_text='address')
     email = forms.EmailInput()
     phone = forms.CharField(max_length=Restaurant.PHONE_MAX_LENGTH,widget=forms.TextInput(attrs={'placeholder': 'Please enter your restaurant’s phone number'}),help_text='phone')
     image = forms.ImageField(required=False, help_text="Upload an image for your restaurant")
     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
     latitude = forms.DecimalField(required=True, widget=forms.HiddenInput())
     longitude = forms.DecimalField(required=True, widget=forms.HiddenInput(),error_messages={'required':'Please select a location for your restaurant!'})


     class Meta:
          model = Restaurant
          exclude = ['slug','owner',]

#A mini form for the menu item
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description']

