from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore
from djangoeats.forms import ProfileForm
from djangoeats.models import Profile
from djangoeats.models import Restaurant
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from djangoeats.forms import ReviewForm
from datetime import datetime




# Create your views here.
def home(request):
    #Display home page
    return render(request, 'djangoeats/home.html')

def login(request):
    #Login functionality for both users and owners?
    return HttpResponse("Login here")

def register(request):
    registered = False 
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
        else:
            print(form.errors)
    else:
        form = ProfileForm()
    return render(request,'djangoeats/register.html',{'form':form, 'registered':registered})


def restaurant(request,restaurant_name_slug):
    context_dict = {}

    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)

        context_dict['restaurant'] = restaurant

    except Restaurant.DoesNotExist:

        context_dict['restaurant'] = None

    return render(request, 'djangoeats/restaurant.html',context=context_dict)
    #Load in details about the given restaurant
    #return HttpResponse("This page will display a specific restaurant")

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
    #Logic that returns a specific dashboard page based on the user logged in
    return HttpResponse("Here's your dashboard. View your favourites or update your restaurants")

def restaurant_edit(request):
    #If not the owner display an error page
    return HttpResponse("Update a restaurant that you own here!")

