//Basic search functionality
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

function clearSearch(){
    ajaxGetRequest("search/?name=&address=&cuisine=", displayCallBack)
}

function searchRestaurants() {	
    //Get inputs
    const nameQuery = document.getElementById('search-name-input').value;
    const addressQuery = document.getElementById('search-address-input').value;
    const cuisineQuery = document.getElementById('search-cuisine-input').value;

    //If no input is made, cancel search
    if (nameQuery == "" && addressQuery == "" && cuisineQuery ==""){
        return;
    }
    
    //Make ajax request and resolve using callback function that formats restaurant tabs
    if (document.URL.includes("djangoeats/")){
        var amendURL = ""
    }
    else{
        var amendURL = "djangoeats/"
    }

    const stringURL = amendURL + "search/?name=" + nameQuery + "&address=" + addressQuery + "&cuisine=" + cuisineQuery;
    ajaxGetRequest(stringURL, displayCallBack)
}


function displayCallBack(response) {
    let str = "";	
    str += String();
    var dashboard = document.URL.includes("dashboard")
    
    if (Object.keys(response['restaurants']).length == 0){
        str += "<h3>Your query had no results :(</h3>";
    }
    else{
    for (restaurant of response['restaurants']){
        str += '<div class="restaurant-card">';
        if (restaurant['image']){
            str +=`<img src="{{ restaurant.image.url|default:'/static/images/logo.png' }}" alt="{{ restaurant.name }} Image">`;
        }
        str += `<h3>` + restaurant['name'] + `</h3>`;
        str += `<p>Cuisine: `+ restaurant['cuisine'] + `</p>`;
        str += `<p>`+ restaurant['address'] + `</p>`;
        str += `<a href="restaurant/`+ restaurant['slug'] + `">View Details</a>\n`;
        if (dashboard){
            str += `<a onclick="removeFavoriteFromDashboard('` + restaurant['slug'] + `')">Remove from Favourites</a>`;
            }
        
        str += `</div>`;
        }
    }
    document.getElementById("restaurant-list").innerHTML = str; 
}


function addFavorite(){
    const stringURL = 'add/?'
    ajaxGetRequest(stringURL, restaurantFavoriteCallBack)
}

function removeFavorite(){
    const stringURL = 'remove/?'
    ajaxGetRequest(stringURL, restaurantFavoriteCallBack)
}

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

function removeFavoriteFromDashboard(restaurant_slug){
    const stringURL = 'remove/?slug=' + restaurant_slug
    ajaxGetRequest(stringURL, displayCallBack)
}
