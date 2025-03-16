
from django.shortcuts import render, get_object_or_404, redirect
from djangoeats.models import Restaurant, MenuItem, Review, UserFavorites, Profile
from django.http import HttpResponse # type: ignore
from djangoeats.forms import ProfileForm
from djangoeats.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from djangoeats.forms import ReviewForm
from datetime import datetime


# Create your views here.


def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'djangoeats/home.html', {'restaurants' : restaurants})

#Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoeats:home')
        else:
            return render(request, 'djangoeats/login.html', {'error': 'Invalid Username or Password'})
    return render(request, 'djangoeats/login.html')



def restaurant(request, restaurant_name_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_name_slug)
    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all()
    context_dict ={}
    context_dict['restaurant'] = restaurant
    context_dict['menu_items'] = menu_items
    context_dict['reviews'] = reviews

    return render(request, 'djangoeats/restaurant.html', context=context_dict)


def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    return username

def logout_view(request):
    username = UserLoggedIn(request)
    if username != None:
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
            return redirect('djangoeats:home')
    else:
        profile_form = ProfileForm()
        user_form = UserForm()
    return render(request, 'djangoeats/register.html', {'user_form': user_form,'profile_form': profile_form})



@login_required
def make_review(request,restaurant_name_slug):
    #POSSIBLY CHECK IF THE USER IS AUTHENTICATED
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
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
            return redirect(reverse('djangoeats:restaurant',
                            kwargs={'restaurant_name_slug':restaurant_name_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'restaurant': restaurant}
    return render(request, 'djangoeats/makeReview.html', context=context_dict)

def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != "owner":
        return redirect('djangoeats:home') # go to home page.

    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'djangoeats/dashboard.html', {'restaurants': restaurants})

def restaurant_edit(request):
    return HttpResponse("Update a restaurant that you own here!")