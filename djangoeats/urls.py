from django.urls import path
from djangoeats import views

app_name = 'djangoeats'

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register,name='register'),
    path('restaurant/<slug:restaurant_slug>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<restaurant_slug>/review',views.make_review,name='make_review'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/search/',views.search,name='dashboard-search'),
    path('restaurant/<restaurant_slug>/update/',views.restaurant_edit,name='restaurant_edit'),
    path('logout/',views.logout_view, name='logout_view'),
    path('search/',views.search,name='search'),
    path('dashboard/register-restaurant/',views.registerRestaurant,name='register_restaurant'),
    path('restaurant/<restaurant_slug>/add-menu-item/',views.addMenuItem,name='add_menu_item'),
    path('dashboard/remove/',views.removeDashboardFavorite, name='removeDashboardFavorite'),
    path('restaurant/<restaurant_slug>/add/',views.addFavorite,name='addFavorite'),
    path('restaurant/<restaurant_slug>/remove/',views.removeFavorite, name='removeFavorite'),
]