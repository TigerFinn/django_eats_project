import json
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

#A models a model, and this one is for the restaurants
class Restaurant(models.Model):
    NAME_MAX_LENGTH = 100
    CUISINE_MAX_LENGTH = 50
    ADDRESS_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 15

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    cuisine = models.CharField(max_length=CUISINE_MAX_LENGTH)
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=PHONE_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True)
    #Holds coordinates for location search
    latitude = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant,self).save(*args,**kwargs)


    def __str__(self):
        return self.name

#User profile
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Owner'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    #Store coordinates for search
    latitude = models.DecimalField(max_digits=30, decimal_places=15, null=False,default=0, blank=False)
    longitude = models.DecimalField(max_digits=30, decimal_places=15, null=False,default=0, blank=False)
    # We never actually implemented the profile picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by', blank=True)


    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


#Menu item
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    #Somewhere down the line adding these wasn't actually implemented
    TYPE_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('drink', 'Drink')
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    
#A review....
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.restaurant.name}"