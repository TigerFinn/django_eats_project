
from django.shortcuts import render, get_object_or_404, redirect
from djangoeats.models import Restaurant, MenuItem, Review, UserFavorites, Profile
from django.http import HttpResponse # type: ignore
from djangoeats.forms import ProfileForm
from django.contrib.auth.decorators import login_required
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoeats:home')
        else:
            return render(request, 'djangoeats/login.html', {'error': 'Invalid Username or Password'})
    return render(request, 'djangoeats/login.html')


#Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoeats:home')
    else:
        form = UserCreationForm()
    return render(request, 'djangoeats/register.html', {'form': form})


def restaurant(request, restaurant_name_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_name_slug)
    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all()
    return render(request, 'djangoeats/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews
    })

# def register(request):
#     registered = False 
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             profile = form.save(commit=False)
#             profile.user = user
#             profile.save()
#         else:
#             print(form.errors)
#     else:
#         form = ProfileForm()
#     return render(request,'djangoeats/register.html',{'form':form, 'registered':registered})


# def restaurant(request,restaurant_name_slug):
#     context_dict = {}

#     try:
#         restaurant = Restaurant.objects.get(slug=restaurant_name_slug)

#         context_dict['restaurant'] = restaurant

#     except Restaurant.DoesNotExist:

#         context_dict['restaurant'] = None

#     return render(request, 'djangoeats/restaurant.html',context=context_dict)
#     #Load in details about the given restaurant
#     #return HttpResponse("This page will display a specific restaurant")

# @login_required
# def make_review(request,restaurant_name_slug):
#     #POSSIBLY CHECK IF THE USER IS AUTHENTICATED
#     try:
#         restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
#     except Restaurant.DoesNotExist:
#         restaurant = None
#     # You cannot add a review to a restaurant that does not exist...
#     if restaurant is None:
#         return redirect(reverse('djangoeats:home'))
    
#     form = ReviewForm()

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)

#     if form.is_valid():
#         if restaurant:
#             review = form.save(commit=False)
#             review.restaurant = restaurant
#             review.reviewer = request.user
#             review.created_at = datetime.now()
#             review.save()
#             return redirect(reverse('djangoeats:restaurant',
#                             kwargs={'restaurant_name_slug':restaurant_name_slug}))
#         else:
#             print(form.errors)
            
#     context_dict = {'form': form, 'restaurant': restaurant}
#     return render(request, 'djangoeats/makeReview.html', context=context_dict

def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != "owner":
        return redirect('djangoeats:home') # go to home page.

    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'djangoeats/dashboard.html', {'restaurants': restaurants})

def restaurant_edit(request):
    return HttpResponse("Update a restaurant that you own here!")


@login_required
def make_review(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = int(request.POST.get('rating'))
        Review.objects.create(reviewer=request.user, restaurant=restaurant, rating=rating, comment=comment)
        return redirect('djangoeats:restaurant_detail', restaurant_slug=restaurant_slug)
    return render(request, 'djangoeats/make_review.html', {'restaurant': restaurant})
