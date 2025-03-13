from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem, Review, UserFavorites, Profile
from django.contrib.auth.decorators import login_required


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
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoeats:home')
    else:
        form = UserCreationForm()
    return render(request, 'djangoeats/register.html', {'form': form})


def restaurant_detail(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    menu_items = restaurant.menu_items.all()
    reviews = restaurant.reviews.all()
    return render(request, 'djangoeats/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews
    })

def make_review(request):
    return HttpResponse("leave a review about a restauraunt")

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
