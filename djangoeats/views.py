
from django.shortcuts import render, get_object_or_404, redirect
from djangoeats.models import Restaurant, MenuItem, Review, Profile
from django.http import HttpResponse # type: ignore
from djangoeats.forms import ProfileForm
from djangoeats.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from djangoeats.forms import ReviewForm
from datetime import datetime
from djangoeats.forms import RestaurantForm
from django.utils.text import slugify
from djangoeats.forms import MenuItemForm, UserForm, ProfileForm

from django.http import JsonResponse

from djangoeats.restaurant_search import basicSearch, query_restaurants
from .haversine import haversine


def home(request):
     restaurants = Restaurant.objects.all()
     return render(request, 'djangoeats/home.html', {'restaurants' : restaurants})

#Login
def login_view(request):
    if UserLoggedIn(request):
        return redirect('djangoeats:home')

    #Get user form submission and log in or throw error
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoeats:dashboard')
        else:
            return render(request, 'djangoeats/login.html', {'error': 'Invalid Username or Password'})
    return render(request, 'djangoeats/login.html')

def logout_view(request):
    username = UserLoggedIn(request)
    if username != None:
        logout(request)
    return redirect('djangoeats:home')


#Handle display of restaurant
def restaurant_detail(request, restaurant_slug):
    #Get relevant info
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    #Required for which buttons need displayed
    if request.user.is_authenticated:
        is_owner = (request.user.profile.user_type.lower() == 'owner')
    else:
        is_owner = False

    reviews = Review.objects.filter(restaurant=restaurant).select_related('reviewer') #That will eagerly load the user attached to each review, so review.user.username works without issues.
    owner_of_restaurant = (request.user == restaurant.owner)
    context_dict ={}
    context_dict['restaurant'] = restaurant
    context_dict['menu_items'] = menu_items
    context_dict['reviews'] = reviews
    context_dict['is_owner'] = is_owner
    context_dict['owner_of_restaurant'] = owner_of_restaurant

    return render(request, 'djangoeats/restaurant.html', context=context_dict)

#Get user registration and create the profile
def register(request):

    if UserLoggedIn(request):
        return redirect('djangoeats:home')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.latitude = profile_form.cleaned_data.get('latitude') 
            profile.longitude = profile_form.cleaned_data.get('longitude')  

            profile.save()

            login(request, user)
            return redirect('djangoeats:dashboard')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        profile_form = ProfileForm()
        user_form = UserForm()
    
    return render(request, 'djangoeats/register.html', {'user_form': user_form, 'profile_form': profile_form})

#Post a review to a web page
@login_required
def make_review(request,restaurant_slug):
    #As per the spec, only customer type users can make reviews
    if request.user.profile.user_type.lower() != 'customer':
        return redirect(reverse('djangoeats:restaurant_detail',kwargs={'restaurant_slug':restaurant_slug}))
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_slug)
    except Restaurant.DoesNotExist:
        restaurant = None
    # You cannot add a review to a restaurant that does not exist...
    if restaurant is None:
        return redirect(reverse('djangoeats:home'))
    
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

    if form.is_valid():
        if restaurant:
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.reviewer = request.user
            review.created_at = datetime.now()
            review.save()
            return redirect(reverse('djangoeats:restaurant_detail',
                            kwargs={'restaurant_slug':restaurant_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'restaurant': restaurant}
    return render(request, 'djangoeats/make_review.html', context=context_dict)

#User dashboard, send a different message based on owner or customer types
@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('djangoeats:home') # go to home page.

    if request.user.profile.user_type.lower() == 'owner':
        restaurants = Restaurant.objects.filter(owner=request.user)
        title = "Your Restaurants"
    else:
        restaurants = request.user.profile.favorite_restaurants.all()
        title = "Your Favorite Restaurants"

    return render(request, 'djangoeats/dashboard.html', {'restaurants': restaurants, 'title':title})


#Register a new restaurant via form
@login_required
def register_restaurant(request):
    # If you are not a owner cannot access this page
    if  not request.user.profile.user_type.lower() == 'owner':
        return redirect(reverse('djangoeats:home'))

    form = RestaurantForm()

    if request.method == 'POST':
        form = RestaurantForm(request.POST)

    if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.latitude = form.cleaned_data.get('latitude') 
            restaurant.longitude = form.cleaned_data.get('longitude')  
            restaurant.save()
            return redirect(reverse('djangoeats:dashboard'))
            
    context_dict = {'form': form}
    return render(request, 'djangoeats/register_restaurant.html', context=context_dict)


#Add menu item to a given restaurant
@login_required
def addMenuItem(request,restaurant_slug):

    restaurant = Restaurant.objects.get(slug=restaurant_slug)
    owner_of_restaurant = (request.user == restaurant.owner)

    #Only want the owner of the restaurant to add menu Items
    if  not owner_of_restaurant:
        return redirect(reverse('djangoeats:home'))
    
    form = MenuItemForm()

    if request.method == 'POST':
        form = MenuItemForm(request.POST)

    if form.is_valid():
        menu_item = form.save(commit=False)
        menu_item.restaurant = restaurant
        menu_item.save()
        return redirect(reverse('djangoeats:restaurant_detail',kwargs={'restaurant_slug':restaurant_slug}))
    
    context_dict = {'form':form,'restaurant':restaurant}
    return render(request , 'djangoeats/add_menu_item.html' , context=context_dict)

#Search method used by ajax-requests.js
def search(request):
    nameQuery = request.GET['name']
    addressQuery = request.GET['address']
    cuisineQuery = request.GET['cuisine']
    #If there are any inputs perform a search, otherwise return all restaurants
        #This case should be handled in ajax_requests.js, this is just a back up
    if nameQuery or addressQuery or cuisineQuery:
        result_list = query_restaurants([nameQuery,addressQuery,cuisineQuery])
    else:
        result_list = list(Restaurant.objects.values())

    #Return a JsonResponse of the filtered restaurants
    return JsonResponse({'restaurants':result_list})

#Order restaurants by their geographical location compared to specified user location
def search_nearby(request):
    user_latitude = float(request.GET.get('lat'))
    user_longitude = float(request.GET.get('lon'))
    restaurants = list(Restaurant.objects.values())
    
    result_list = []

    #For each restaurant find distance from user
    for restaurant in restaurants:
        distance = haversine(float(user_latitude), float(user_longitude), float(restaurant['latitude']), float(restaurant['longitude']))
        result_list.append({
            "name": restaurant['name'],
            "address": restaurant['address'],
            "cuisine": restaurant['cuisine'],
            "latitude": restaurant['latitude'],
            "longitude": restaurant['longitude'],
            "distance": distance,
            "slug": restaurant['id'],
        })
    
    #Sort list by distance of restaurant
    result_list.sort(key=lambda x: x['distance'])
    if request.user.profile.user_type == "Owner":
        owner = True
    else:
        owner = False
   
    return JsonResponse({'restaurants': result_list, 'owner': owner})



#Take a restaurant name and remove it from the favorites of the current user - called by JS
def remove_dashboard_favorite(request):
    restaurant_slug=request.GET['slug']

    #Find the restaurant and remove
    for r in request.user.profile.favorite_restaurants.values():
        if r['slug'] == restaurant_slug:
            request.user.profile.favorite_restaurants.remove(Restaurant.objects.get(slug=r['slug']))
            return JsonResponse({'restaurants':list(request.user.profile.favorite_restaurants.values())})
  
    return JsonResponse({'restaurants':list(request.user.profile.favorite_restaurants.values())})

#Add restaurant to user favourite - called by JS
def add_favorite(request, restaurant_slug):
    for r in Restaurant.objects.values():
        if r['slug'] == restaurant_slug:
            request.user.profile.favorite_restaurants.add(Restaurant.objects.get(slug=r['slug']))
            break
    return JsonResponse({'newText':"Remove from Favourites", 'function':"removeFavorite()"})

#Remove restaurant from user favourite - called by JS
def remove_favorite(request, restaurant_slug):
    for r in request.user.profile.favorite_restaurants.values():
        if r['slug'] == restaurant_slug:
            request.user.profile.favorite_restaurants.remove(Restaurant.objects.get(slug=r['slug']))
            break    
    
    return JsonResponse({'newText':"Add to Favourites", 'function':"addFavorite()"})


#Helper method
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    return username