from django.urls import path
from djangoeats import views

app_name = 'djangoeats'

urlpatterns = [
    #Homepage actions - search & user auth
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register,name='register'),
    path('search_nearby/', views.search_nearby, name='search_nearby'),
    path('logout/',views.logout_view, name='logout_view'),
    path('search/',views.search,name='search'),

    #Restaurant actions - view, review, favourite actions & menu adding
    path('restaurant/<slug:restaurant_slug>/', views.restaurant_detail, name='restaurant_detail'), #If this ever changes, go change displayCallback in ajax_requests.js
    path('restaurant/<slug:restaurant_slug>/review',views.make_review,name='make_review'),
    path('restaurant/<slug:restaurant_slug>/add/',views.add_favorite,name='add_favorite'),
    path('restaurant/<slug:restaurant_slug>/remove/',views.remove_favorite, name='remove_favorite'),
    path('restaurant/<slug:restaurant_slug>/add-menu-item/',views.addMenuItem,name='add_menu_item'),

    #Dashboard actions - user dashboard, register a restaurant, favorite actions
    path('dashboard/',views.dashboard,name='dashboard'),
    # path('dashboard/search/',views.search,name='dashboard_search'),
    path('dashboard/register-restaurant/',views.register_restaurant,name='register_restaurant'),
    path('dashboard/remove/',views.remove_dashboard_favorite, name='remove_dashboard_favorite'),
]