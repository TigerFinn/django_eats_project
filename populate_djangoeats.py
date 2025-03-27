import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_eats_project.settings')

import django
django.setup()
from djangoeats.models import Profile, Restaurant, MenuItem, Review
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


def populate():
    users = [
        {'type':"Customer",'username':"A_Customer",'email':"A_Person@place.com",'lat':55.8731, 'lon':-4.2923},
        {'type':"Customer",'username':"Another_Customer",'email':"A.P.1234@definitely.real",'lat':55.9497, 'lon':-3.2009},
        {'type':"Owner",'username':"Jim",'email':"admin@jimsfoodplaces.com",'lat':0, 'lon':0},
        {'type':"Owner",'username':"Jill",'email':"jill@business.co.uk",'lat':0, 'lon':0},
    ]

    restaurants = [
        {'owner':"Jim", 'name':"Good Food Place",'cuisine':"British",'address':"12 Good Food Road, Glasgow, G99 1JL",
        'email':"goodfoodinfo@jimsfood.com",'phone':1234567890,'lat':55.8727, 'lon':-4.2910},
        {'owner':"Jim", 'name':"Better Food Place",'cuisine':"Italian",'address':"34 Dessert Island, Edinburgh, E46 2KZ",
        'email':"betterfoodinfo@jimsfoodplace.com",'phone':9876543210,'lat':55.9500, 'lon':-3.1885},
        {'owner':"Jill", 'name':"FoodMadeHere",'cuisine':"Indian",'address':"34 Curry Lane, Glasgow, G24 3LA",
        'email':"jill@foodmadehere.com",'phone':5432109876,'lat':55.8643, 'lon': -4.2501},
    ]

    goodFoodPlaceMenuItems = [
        {'name':"Fish & Chips",'description':"Classic fish and chips",'price':12.50,'type':"main"},
        {'name':"Smoked Sausage",'description':"Does what it says on the tin",'price':5.30,'type':"main"},
        {'name':"Deep Fried Mars Bar",'description':"Do you value your health? We don't",'price':4.75,'type':"main"},
        {'name':"Steak Pie",'description':"Simply the best",'price':9.00,'type':"main"},
        {'name':"Shepherd's Pie",'description':"It's mince and tatties but as a pie!",'price':6.99,'type':"main"},
        {'name':"Mushy Peas",'description':"Garden peas mushed up with salt",'price':1.50,'type':"starter"},
        {'name':"Soup of the Day",'description':"Please see signage for type of soup",'price':6.00,'type':"starter"},
        {'name':"Chip butty",'description':"Chips on a roll",'price':3.50,'type':"starter"},
        {'name':"Water",'description':"H2O with ice",'price':0.0,'type':"drink"},
        {'name':"Juice",'description':"Orange, apple or both",'price':1.50,'type':"drink"},
        {'name':"Tea",'description':"Tea, innit",'price':1.50,'type':"drink"},
    ]

    betterFoodPlaceMenuItems = [
        {'name':"10\" pizza",'description':"Margherita, pepperoni or veggie",'price':9.50,'type':"main"},
        {'name':"14\" pizza",'description':"Margherita, pepperoni or veggie",'price':13.50,'type':"main"},
        {'name':"Carbonara",'description':"Linguini pasta with carbonara sauce",'price':8.75,'type':"main"},
        {'name':"Lasagne",'description':"Layers of overrated food",'price':11.00,'type':"main"},
        {'name':"Risotto",'description':"I think it's rice as a funky meal",'price':7.99,'type':"main"},
        {'name':"Mini Gnocci",'description':"Mini potato pasta",'price':5.50,'type':"starter"},
        {'name':"Larger Gnocci",'description':"Bigger potato pasta (but with less)",'price':5.50,'type':"starter"},
        {'name':"Carprese salad",'description':"Do you value your health? We do",'price':3.50,'type':"starter"},
        {'name':"Water",'description':"Ice with added H2O",'price':0.15,'type':"drink"},
        {'name':"Juice",'description':"Cranberry, Pineapple or both",'price':1.50,'type':"drink"},
        {'name':"Coffee",'description':"Some would say it's better than tea",'price':1.50,'type':"drink"},
    ]

    foodMadeHereMenuItems = [
        {'name':"Chicken Curry",'description':"Tasty but spicy",'price':9.50,'type':"main"},
        {'name':"Veggie Curry",'description':"Just as tasty, just as spicy",'price':9.50,'type':"main"},
        {'name':"Lamb Curry",'description':"Slightly less tasty, slightly more spicy",'price':9.75,'type':"main"},
        {'name':"Chicken Korma",'description':"Less tasty, less spicy",'price':9.50,'type':"main"},
        {'name':"Veggie Korma",'description':"Less tasty, less meaty, less spicy",'price':9.50,'type':"main"},
        {'name':"Naan bread",'description':"Tasty garlic naan",'price':1.50,'type':"starter"},
        {'name':"Rice",'description':"Rice cooked in veggie stock",'price':1.50,'type':"starter"},
        {'name':"Pakora",'description':"Chicken or veggie",'price':3.50,'type':"starter"},
        {'name':"Water",'description':"H2O",'price':0.00,'type':"drink"},
        {'name':"Juice",'description':"Pineapple, dragonfruit or pomegranite",'price':1.50,'type':"drink"},
        {'name':"Tea and Coffee",'description':"If you can't choose which, have both in one :)",'price':1.50,'type':"drink"},
    ]

    restaurant_menus = []
    rests = {
        'Good Food Place':goodFoodPlaceMenuItems,
        'Better Food Place':betterFoodPlaceMenuItems,
        'FoodMadeHere':foodMadeHereMenuItems,
    }

    for u in users:
        add_profile(u)
        print("Profile added: " + u['username'])

    for r in restaurants:
        owner = User.objects.get(username = r['owner'])
        restaurant = add_restaurant(owner, r['name'], r['cuisine'],r['address'],r['email'], r['phone'], r['lat'], r['lon'])
        restaurant_menus.append(restaurant)
        print(restaurant.name + ".... created")

    for rm in restaurant_menus:
        for item in rests[rm.name]:
            add_menu_item(rm, item['name'], item['description'], item['price'], item['type'])
        print(rm.name + ".... menu created")


    reviews = [{'user':"A_Customer",'restaurant':"Good Food Place",'description':"AMAZING FOOD. MY favourite PLACE!",'rating':5},
               {'user':"Another_Customer",'restaurant':"Good Food Place",'description':"Horrific food. Why are the peas mushed?",'rating':1},
               {'user':"A_Customer",'restaurant':"Better Food Place",'description':"It's alright",'rating':3},
               {'user':"A_Customer",'restaurant':"FoodMadeHere",'description':"Are you sure you can call that food?",'rating':1},
               ]

    favourites = [{'user':"A_Customer",'restaurant':"Good Food Place"}, {'user':'A_Customer','restaurant':"Better Food Place"},
                  {'user':"Another_Customer",'restaurant':"Better Food Place"}]
    
    for r in reviews:
        add_review(User.objects.get(username = r['user']), Restaurant.objects.get(name = r['restaurant']), r['description'],r['rating'])

    for f in favourites:
        add_user_favourite(User.objects.get(username = f['user']), Restaurant.objects.get(name = f['restaurant']))




def add_profile(u):
    user =  User.objects.get_or_create(username = u['username'], email = u['email'])[0]
    user.set_password("1234")
    user.save()
    p = Profile.objects.get_or_create(user = user, user_type = u['type'], latitude = u['lat'], longitude = u['lon'])[0]
    p.save()
    return p

def add_restaurant(owner,name,cuisine,address,email,phone,lat,lon):
    r = Restaurant.objects.get_or_create(owner = owner, name = name, cuisine = cuisine, address = address, email = email, phone = phone,latitude=lat,longitude=lon)[0]
    r.slug = slugify(name)
    r.menu = ""
    r.save()
    return r

def add_menu_item(restaurant, name, description, price, type):
    m = MenuItem.objects.get_or_create(restaurant = restaurant, name = name, description = description, price = price, type = type)[0]
    m.save()
    return m

def add_user_favourite(user, restaurant):
    p = Profile.objects.get_or_create(user=user)[0]
    p.favorite_restaurants.add(restaurant)
    p.save()

    return user

def add_review(user, restaurant, description, rating):
    r = Review.objects.get_or_create(reviewer = user, restaurant = restaurant, comment =  description, rating = rating)[0]

    r.save()
    return r

def main():
    populate()

if __name__ == "__main__":
    print("Starting djangoeats population script...")
    populate()