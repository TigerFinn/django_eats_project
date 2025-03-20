import json
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    NAME_MAX_LENGTH = 100
    CUISINE_MAX_LENGTH = 50
    ADDRESS_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 15

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    cuisine = models.CharField(max_length=CUISINE_MAX_LENGTH)
    menu = models.TextField(blank=True)
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=PHONE_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Owner'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by', blank=True)


    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    TYPE_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('drink', 'Drink')
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


# class UserFavorites(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by', blank=True)

#     def __str__(self):
#         return self.user.username
    

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.restaurant.name}"