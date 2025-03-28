//Basic search functionality, takes a url, makes an ajax request to it, passes the result into a callback function
function ajaxGetRequest(stringURL, callback){
    var xhttp= new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }       
    };
    xhttp.open("GET",stringURL, true);
    
    xhttp.send();	
}

//Redisplay all the restaurants
function clearSearch(){
    ajaxGetRequest(blankURL_Amender() + "search/?name=&address=&cuisine=", displayCallBack)
}

//search restaurants based on name, address and cuisine that is gotten from the page
function searchRestaurants() {	
    //Get inputs
    const nameQuery = document.getElementById('search-name-input').value;
    const addressQuery = document.getElementById('search-address-input').value;
    const cuisineQuery = document.getElementById('search-cuisine-input').value;

    //If no input is made, cancel search
    if (nameQuery == "" && addressQuery == "" && cuisineQuery ==""){
        return;
    }
    
    
    // Call the ajax request for a basic search
    const stringURL = blankURL_Amender() + "search/?name=" + nameQuery + "&address=" + addressQuery + "&cuisine=" + cuisineQuery;
    ajaxGetRequest(stringURL, displayCallBack)
}


//Search for restaurants based on the users location.
function searchNearby() {
    //Get lat and lon
    const userLat = document.getElementById('user-latitude').value;
    const userLon = document.getElementById('user-longitude').value;

    //Make ajax request with basic display callback
    const stringURL = blankURL_Amender() + "search_nearby/?lat=" + userLat + "&lon=" + userLon;
    ajaxGetRequest(stringURL, displayCallBack);
}

//Janky display call back that takes a json input and will format a list of restaurants
//Couldn't figure out how to get it to call nicely without updating everything
    //I could have used the {% include %} template but that did not allow for the {% restaurant_action_block %} to work.
function displayCallBack(response) {
    let str = "";	
    str += String();
    //Boolean that will allow reload of restaurants to a customer dashboard
    var dashboard = document.URL.includes("dashboard")
    
    //Nothing to display
    if (Object.keys(response['restaurants']).length == 0){
        str += "<h3>Your query had no results :(</h3>";
    }
    //Reformat each restaurant
    else{
    for (restaurant of response['restaurants']){
        str += '<div class="restaurant-card">';
        str += `<h3>` + restaurant['name'] + `</h3>`;
        str += `<p>Cuisine: `+ restaurant['cuisine'] + `</p>`;
        str += `<p>`+ restaurant['address'] + `</p>`;
        //Reconstruct href (not ideal, but can't parse template language using JS)
        str += `<a href="/djangoeats/restaurant/` + restaurant['slug'] + `">View Details</a>`;
        //For customers on dashboard
        if (dashboard){
            str += `<a onclick="removeFavoriteFromDashboard('` + restaurant['slug'] + `')">Remove from Favourites</a>`;
            }
        
        str += `</div>`;
        }
    }
    document.getElementById("restaurant-list").innerHTML = str; 
}

//These functions are for the restaurant page when a customer adds or removes a restaurant from favourites
function addFavorite(){
    const stringURL = 'add/?'
    ajaxGetRequest(stringURL, restaurantFavoriteCallBack)
}

function removeFavorite(){
    const stringURL = 'remove/?'
    ajaxGetRequest(stringURL, restaurantFavoriteCallBack)
}

// Callback will redisplay 'favourite' button to be able to be added or removed
function restaurantFavoriteCallBack(response){
    let str = "";
    str += String();
    str +=`<form onsubmit = "`;
    str+= response['function'];
    str +=`"><input type="submit" value = "`;
    str += response['newText'];
    str+= `"/></form>`;
    str+= `<h1>A TEST</h1>`;
    document.getElementById('add-or-remove').innerHTML = str;
}

// Function removes a restaurant from a user's favourites and deletes it from their dashboard
function removeFavoriteFromDashboard(restaurant_slug){
    const stringURL = 'remove/?slug=' + restaurant_slug
    ajaxGetRequest(stringURL, displayCallBack)
}

function blankURL_Amender(){
    if (document.URL.includes("djangoeats/")) {
        return "";
    } else {
        return "djangoeats/";
    }
}