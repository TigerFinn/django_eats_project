from django.contrib import admin
from .models import Profile, Restaurant, MenuItem, Review, UserFavorites

admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(UserFavorites)
admin.site.register(Review)
