from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore



# Create your views here.
def home(request):
    #Display home page
    return render(request, 'djangoeats/home.html')

def login(request):
    #Login functionality for both users and owners?
    return HttpResponse("Login here")

def register(request):
    #register functionality for both users and owners?
    return HttpResponse("Register here")

def restaurant(request):
    #Load in details about the given restaurant
    return HttpResponse("This page will display a specific restaurant")

def make_review(request):
    return HttpResponse("Here you can make a review about a restauraunt")

def dashboard(request):
    #Logic that returns a specific dashboard page based on the user logged in
    return HttpResponse("Here's your dashboard. View your favourites or update your restaurants")

def restaurant_edit(request):
    #If not the owner display an error page
    return HttpResponse("Update a restaurant that you own here!")

