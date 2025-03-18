
from django.shortcuts import render, get_object_or_404, redirect
from djangoeats.models import Restaurant, MenuItem, Review, UserFavorites, Profile
from django.http import HttpResponse # type: ignore
from djangoeats.forms import ProfileForm
from djangoeats.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from djangoeats.forms import ReviewForm, RegisterForm
from datetime import datetime


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('djangoeats:dashboard')
    return redirect('djangoeats:register')


#Login
def login_view(request):
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



def restaurant_detail(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all()


    context_dict ={
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews
    }

    return render(request, 'djangoeats/restaurant.html', context=context_dict)



def logout_view(request):
    logout(request)
    return redirect('djangoeats:home')

# Register
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('djangoeats:dashboard')
    else:
        profile_form = ProfileForm()
        user_form = UserForm()
    return render(request, 'djangoeats/register.html', {'user_form': user_form,'profile_form': profile_form})



@login_required
def make_review(request,restaurant_slug):
    #POSSIBLY CHECK IF THE USER IS AUTHENTICATED
    restaurant = get_object_or_404(slug=restaurant_slug)
    form = ReviewForm(request.POST or None)



    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.restaurant = restaurant
        review.reviewer = request.user
        review.created_at = datetime.now()
        review.save()
        return redirect('djangoeats:restaurant_detail', restaurant_slug=restaurant.slug)
    return render(request, 'djangoeats/makeReview.html', {'form': form, 'restaurant': restaurant})


@login_required
def dashboard(request):

    featured_restaurants = Restaurant.objects.all()[:5]

    # profile = Profile.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return redirect('djangoeats:home') # go to home page.

    if request.user.profile.user_type == 'owner':
        restaurants = Restaurant.objects.filter(owner=request.user)
    else:
        user_favorites, created = UserFavorites.objects.get_or_create(user=request.user)
        restaurants = user_favorites.favorite_restaurants.all()


    return render(request, 'djangoeats/dashboard.html', {
        'restaurants': restaurants,
        'featured_restaurants': featured_restaurants,
        })

#Pass restaurant and menu items in to the edit restaurant page
def restaurant_edit(request, restaurant_slug):
    if request.user.profile.user_type == 'owner':
        redirect('djangoeats:home')
    user_favorites, created = UserFavorites.objects.get_or_create(user=request.user)
    restaurants = user_favorites.favorite_restaurants.all()

    context_dict = {'restaurants': restaurants}

    return render(request, 'djangoeats/restaurant_edit.html', context = context_dict)


def search(request):
    query = request.GET.get('q', '')
    results = Restaurant.objects.filter(name__icontains=query)
    return render(request, 'djangoeats/search_results.html', {'results': results})


def favorites(request):
    user_favorites, created = UserFavorites.objects.get_or_create(user=request.user)
    return render(request, 'djangoeats/favorites.html', {'favorites': user_favorites.favorite_restaurants.all()})

