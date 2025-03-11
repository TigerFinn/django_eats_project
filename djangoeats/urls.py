from django.urls import path
from djangoeats import views

app_name = 'djangoeats'

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('restaurant/<restaurant_slug>/',views.restaurant,name='restaurant'),
    path('restaurant/<restaurant_slug>/review',views.make_review,name='make_review'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('restaurant/<restaurant_slug>/update',views.restaurant_edit,name='restaurant_edit'),
]