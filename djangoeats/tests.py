from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from djangoeats.models import Restaurant
from djangoeats.models import User
from djangoeats.models import Profile
from djangoeats.models import MenuItem
from djangoeats.models import Review
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

# Create your tests here.

class RestaurantMethodsTests(TestCase):

    def test_slug_line_creation(self):
        #Test to see if The slug for the restaurant is made correctly
        user_profile = create_profile("owner1","owner1@letter.com","owner",37.8926,-122.4849)
        restaurant = create_restaurant(user_profile.user,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

        self.assertEqual(restaurant.slug,"cooked-food-store")

class RestaurantViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_profile = create_profile("owner1","owner1@letter.com","owner",37.8926,-122.4849)
        restaurant = create_restaurant(user_profile.user,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)
        #Didnt Work when I put owner with a lower case o , so might want to fix that
        cls.user = user_profile.user
        cls.restaurant = restaurant

    #def setUp(self):
    #   self.response = self.client.get(reverse('djangoeats:restaurant_detail',kwargs={"restaurant_slug":self.restaurant.slug}))

    def test_apprpriate_owner_of_restaurant_buttons_present(self):
        login_user(self,'owner1')
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['is_owner'],True)
        self.assertEqual(response.context["owner_of_restaurant"],True)
        #Should Contain ability to add menu items to the Restaurant or return Home
        self.assertContains(response,"Add a Menu Item")
        self.assertContains(response,"Return Home")
        #Customer buttons should not be on the Html 
        self.assertNotContains(response,"Add to Favorites")
        self.assertNotContains(response,"Make your Review")

    def test_appropriate_owner_buttons_present(self):
        user_profile = create_profile("owner2","owner2@letter.com","owner",37.8926,-122.4849)
        login_user(self,"owner2")
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['is_owner'],True)
        self.assertEqual(response.context["owner_of_restaurant"],False)
        #Owners can return Home
        self.assertContains(response,"Return Home")
        #Owner of Restaurant and Customer buttons are not accesible for a owner
        self.assertNotContains(response,"Add a Menu Item")
        self.assertNotContains(response,"Add to Favorites")
        self.assertNotContains(response,"Make your Review")

    def test_appropriate_customer_buttons_present(self):
        create_customer()
        login_user(self,"customer1")
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['is_owner'],False)
        self.assertEqual(response.context["owner_of_restaurant"],False)
        #Customers can return Home , Add to favourites and make a review 
        self.assertContains(response,"Return Home")
        self.assertContains(response,"Add to Favorites")
        self.assertContains(response,"Make your Review")
        #Customers cannot add a menu item to the restaurant
        self.assertNotContains(response,"Add a Menu Item")

    def test_appropriate_anonymous_buttons_present(self):
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['is_owner'],False)
        self.assertEqual(response.context["owner_of_restaurant"],False)
        #Owners can return Home , Add to favourites and make a review 
        self.assertContains(response,"Return Home")
        #Customers cannot add a menu item to the restaurant
        self.assertNotContains(response,"Add a Menu Item")
        self.assertNotContains(response,"Add to Favorites")
        self.assertNotContains(response,"Make your Review")

    

    def test_correct_restaurant_information(self):
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['restaurant'],self.restaurant)
        self.assertContains(response,"Cooked Food Store")
        self.assertContains(response,"owner1")

    def test_restaurant_without_menu_items(self):
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['menu_items'],[])
        self.assertContains(response,"No Menu Items available.")

    def test_restaurant_with_menu_items(self):
        add_menu_item(self.restaurant,"Toast","Cooked Bread",1.00,"starter")
        add_menu_item(self.restaurant,"Cheesy Toast","Cooked Bread with cheese",2.00,"main")
        add_menu_item(self.restaurant,"Toast Milkshake","Grinded Cooked Bread",1.00,"drink")

        response = get_slug_response(self,'restaurant_detail')


        self.assertContains(response,"Toast")
        self.assertContains(response,"Cheesy Toast")
        self.assertContains(response,"Toast Milkshake")

        num = len(response.context['menu_items'])
        self.assertEqual(num,3)

    def test_restaurant_with_no_reviews(self):
        response = get_slug_response(self,'restaurant_detail')

        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['reviews'],[])
        self.assertContains(response,"No reviews yet.")
    
    
    def test_restaurant_with_reviews(self):
        customer1 = create_customer()
        customer2 = create_profile("customer2","customer2@letter.com","customer",36.8926,-121.4849).user

        create_review(customer1,self.restaurant,"Wicked meal and a proper steal ;)",5)
        create_review(customer2,self.restaurant,"Not terrible , Not amazing",2)

        response = get_slug_response(self,'restaurant_detail')

        self.assertContains(response,"customer1")
        self.assertContains(response,"Wicked meal and a proper steal ;)")
        self.assertContains(response,"customer2")
        self.assertContains(response,"Rating: 2 ⭐")
        num = len(response.context['reviews'])
        self.assertEqual(num,2)



class RegisterRestaurantViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        owner_profile = create_profile("owner1","owner1@letter.com","owner",37.8926,-122.4849)
        customer_profile = create_profile("customer1","customer1@letter.com","customer",36.8926,-121.4849)
        cls.owner_user = owner_profile.user
        cls.customer_user = customer_profile.user

    def test_customer_redirected_to_home(self):
        login_user(self,"customer1")
        response = self.client.get(reverse('djangoeats:register_restaurant'))

        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response,reverse('djangoeats:home'))

    #def test_anonymous_redirected_to_home(self):
    #   response = self.client.get(reverse('djangoeats:register_restaurant'))

 #        self.assertEqual(response.status_code , 302)
 #       self.assertRedirects(response,reverse('djangoeats:login_view'))


    def test_owner_redirected_to_form(self):
        login_user(self,"owner1")
        response = self.client.get(reverse('djangoeats:register_restaurant'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Add a restaurant")


    def test_submit_make_restaurant_form(self):
        
        input_data = {
            'name': 'Nibble Restaurant',
            'cuisine': 'Italian',
            'address': '123 Food Street',
            'email': 'food@nibble.com',
            'phone': '1234567890',
            'latitude': 40.7128,
            'longitude': -74.0060,
        }
        login_user(self,"owner1")
        response = self.client.post(reverse('djangoeats:register_restaurant'), data=input_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('djangoeats:dashboard'))
        self.assertTrue(Restaurant.objects.filter(name="Nibble Restaurant").exists())
        num=len(Restaurant.objects.all())
        self.assertEqual(num,1)


    def test_submit_invalid_restaurant_form(self):
        input_data = {
            'name': 'Nibble Restaurant',
            'cuisine': 'Italian',
            'address': '123 Food Street',
            'email': 'food@nibble.com',
            'phone': '12345678901234567890',#phone number too long
            'latitude': 21.2342,
            'longitude': -74.0060,
        }
        login_user(self,"owner1")
        response = self.client.post(reverse('djangoeats:register_restaurant'), data=input_data)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Add a restaurant")

class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner_user = create_owner()

    def test_valid_login(self):
        input_data = {
            'username':'owner1',
            'password':'1234'
        }

        response = self.client.post(reverse('djangoeats:login_view'), data=input_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:dashboard'))
    
    def test_invalid_login(self):
        input_data = {
            'username':'SmokingSnail42o',
            'password':'4321'
        }

        response = self.client.post(reverse('djangoeats:login_view'), data=input_data)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Log in and explore the best restaurants.")

    def test_anonymous_accessing_view(self):
        response = self.client.get(reverse('djangoeats:login_view'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Log in and explore the best restaurants.")

    def test_logged_in_user_accessing_login_view(self):
        login_user(self,"owner1")
        response = self.client.get(reverse('djangoeats:login_view'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:home'))

class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner_user = create_owner()

    def test_logged_in_user_accessing_logout_view(self):
        login_user(self,"owner1")
        response = self.client.get(reverse('djangoeats:logout_view'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:home'))
        response = self.client.get(reverse('djangoeats:home'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_anonymous_user_accessing_logout_view(self):
        response = self.client.get(reverse('djangoeats:logout_view'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:home'))

class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner_user = create_owner()

    def test_logged_in_user_accessing_register_view(self):
        login_user(self,"owner1")
        response = self.client.get(reverse('djangoeats:register'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:home'))

    
    def test_anonymous_user_accessing_register_view(self):
        response = self.client.get(reverse('djangoeats:register'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Join DjangoEats!')

    def test_successful_user_registration(self):
        input_data = {
            'username':'Newcustomer',
            'email':'new@old.com',
            'password':'password123',
            'user_type':'customer',
            'latitude': 21.2342,
            'longitude': -74.0060,
        }
        response = self.client.post(reverse('djangoeats:register'), data=input_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:dashboard'))
        self.assertEqual(User.objects.filter(username="Newcustomer").exists(),True)
        num = len(User.objects.all())
        self.assertEqual(num,2)

    def test_unsuccessful_user_registration(self):
        input_data = {
            'username':'Newcustomer',
            'email':'justwrong',#incorrect Email Input
            'password':'password123',
            'user_type':'customer',
            'latitude': 21.2342,
            'longitude': -74.0060,
        }
        response = self.client.post(reverse('djangoeats:register'), data=input_data)
        self.assertEqual(response.status_code,200)
        self.assertFormError(response, 'user_form', 'email', 'Enter a valid email address.')

        #Writing is coming from here


class addMenuItemViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() 
        create_customer()
        owner = create_owner()
        cls.restaurant = create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

    def test_successful_menu_item_add(self):
        input_data = {
            'name':"Scone",
            'description':"bread but sweet",
            'price':2.50,
            'type':"starter"
        }
        before_sum = len(MenuItem.objects.all())
        login_user(self,"owner1")
        response = self.client.post(url_with_slug(self,'add_menu_item'), data=input_data)
        self.assertRedirects(response,url_with_slug(self,'restaurant_detail'))
        self.assertEqual(len(MenuItem.objects.all()),before_sum + 1)
        self.assertEqual(MenuItem.objects.filter(restaurant=self.restaurant).exists(),True)

    def test_not_owner_of_restaurant(self):
        login_user(self,"customer1")
        response = get_slug_response(self,'add_menu_item')
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('djangoeats:home'))

    def test_owner_of_restaurant_can_get_form(self):
        login_user(self,"owner1")
        response = get_slug_response(self,'add_menu_item')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,f"Add a Menu Item to {self.restaurant.name}")

class MakeReviewViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() 
        create_customer()
        owner = create_owner()
        cls.restaurant = create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

    
    def test_successful_make_review(self):
        input_data = {
            'comment':"Not bad grub.",
            'rating':3,
        }
        before_sum = len(Review.objects.all())
        login_user(self,"customer1")
        response = self.client.post(url_with_slug(self,'make_review'), data=input_data)
        self.assertRedirects(response,url_with_slug(self,'restaurant_detail'))
        self.assertEqual(len(Review.objects.all()),before_sum + 1)

    def test_not_customer(self):
        login_user(self,"owner1")
        response = get_slug_response(self,'make_review')
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,url_with_slug(self,'restaurant_detail'))

    def test_customer_can_get_form(self):
        login_user(self,"customer1")
        response = get_slug_response(self,'make_review')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Share your Opinion on the Restaurant")



class DashboardViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        customer = create_customer()
        owner = create_owner()

        restaurant1 = create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)
        create_restaurant(owner,"Food Store","Italian","26 Lebron street", "wearealso@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

        add_user_favourite(customer,restaurant1)
    
    def test_owner_dashboard(self):
        login_user(self,"owner1")
        response = self.client.get(reverse('djangoeats:dashboard'))

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(response.context['restaurants']),2)
        self.assertContains(response,"Cooked Food Store")
        self.assertContains(response,"Food Store")
        self.assertContains(response,"Register Your Restaurant")
        self.assertContains(response,"Add menu item")

    def test_customer_dashboard(self):
        login_user(self,"customer1")
        response = self.client.get(reverse('djangoeats:dashboard'))

        self.assertEqual(response.status_code , 200)
        self.assertEqual(len(response.context['restaurants']),1)
        self.assertContains(response,"Cooked Food Store")
        self.assertContains(response,"Remove from Favourites")


class RemoveDashboardFavouriteViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        customer = create_customer()
        owner = create_owner()

        restaurant1 = create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)
        restaurant2 = create_restaurant(owner,"Food Store","Italian","26 Lebron street", "wearealso@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

        add_user_favourite(customer,restaurant1)
        add_user_favourite(customer,restaurant2)

        cls.restaurant1 = restaurant1

    def test_remove_dashboard_favourite(self):

        login_user(self,"customer1")
        response = self.client.get(reverse('djangoeats:dashboard'))
        self.assertEqual(len(response.context['restaurants']),2)

        response = self.client.get(reverse('djangoeats:removeDashboardFavorite'),{'slug': self.restaurant1.slug})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Parse JSON response
        response_data = response.json()
        self.assertEqual(len(response_data['restaurants']), 1)
        remaining_slugs = [r['slug'] for r in response_data['restaurants']]
        self.assertNotIn(self.restaurant1.slug, remaining_slugs)
        
class AddFavoriteTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        customer = create_customer()
        owner = create_owner()

        restaurant1 = create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)
        restaurant = create_restaurant(owner,"Food Store","Italian","26 Lebron street", "wearealso@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

        add_user_favourite(customer,restaurant1)

        cls.restaurant = restaurant


class HomeviewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_customer()
        owner = create_owner()

        create_restaurant(owner,"Cooked Food Store","Indian","23 Lebron street", "weare@LebronStreet.com", 74156789120 ,37.8921,-122.4837)
        create_restaurant(owner,"Food Store","Italian","26 Lebron street", "wearealso@LebronStreet.com", 74156789120 ,37.8921,-122.4837)

    def test_Logged_in_buttons_present(self):
        login_user(self,"customer1")
        response = self.client.get(reverse('djangoeats:home'))
        self.assertContains(response,"Dashboard")
        self.assertContains(response,"Log Out")
        self.assertContains(response,"Welcome, customer1")

    def test_Logged_out_buttons_present(self):
        response = self.client.get(reverse('djangoeats:home'))
        self.assertContains(response,"Log In")
        self.assertContains(response,"Register")

    def test_Restaurants_are_displayed(self):
        response = self.client.get(reverse('djangoeats:home'))
        self.assertEqual(len(response.context['restaurants']) , 2)
        self.assertContains(response,"Cooked Food Store")
        self.assertContains(response,"Food Store")

def create_customer():
    return create_profile("customer1","customer1@letter.com","customer",36.8926,-121.4849).user

def create_owner():
    return create_profile("owner1","owner1@letter.com","owner",37.8926,-122.4849).user


def get_slug_response(currentTest,path_name):
    return currentTest.client.get(url_with_slug(currentTest,path_name))

def url_with_slug(currentTest,path_name):
    return reverse(f'djangoeats:{path_name}',kwargs={'restaurant_slug':currentTest.restaurant.slug})



def login_user(current_test , username):
    current_test.client.login(username=username,password="1234")



def create_profile(username,email,user_type,latitude,longitude):
    user =  User.objects.get_or_create(username = username, email = email)[0]
    user.set_password("1234")
    user.save()
    p = Profile.objects.get_or_create(user = user, user_type = user_type, latitude = latitude, longitude = longitude)[0]
    p.save()
    return p

def create_restaurant(owner,name,cuisine,address,email,phone,lat,lon):
    r = Restaurant.objects.get_or_create(owner = owner, name = name, cuisine = cuisine, address = address, email = email, phone = phone,latitude=lat,longitude=lon)[0]
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

def create_review(user, restaurant, description, rating):
    r = Review.objects.get_or_create(reviewer = user, restaurant = restaurant, comment =  description, rating = rating)[0]
    r.save()
    return r

