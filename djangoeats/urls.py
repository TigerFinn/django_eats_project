from django.urls import path
from djangoeats import views

app_name = 'djangoeats'

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register,name='register'),
    path('restaurant/<restaurant_name_slug>/',views.restaurant,name='restaurant'),
    path('restaurant/<restaurant_name_slug>/review',views.make_review,name='make_review'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('restaurant/<restaurant_name_slug>/update',views.restaurant_edit,name='restaurant_edit'),
    path('logout',views.logout_view, name='logout_view'),
]