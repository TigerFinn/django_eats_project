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
    var searchURL = "search/?name=" + nameQuery + "&address=" + addressQuery + "&cuisine=" + cuisineQuery;
    ajaxGetRequest(searchURL, displayCallBack)
}

function displayCallBack(response) {
    let str = "";	
    str += String();
    // document.getElementById("restaurant-list").innerHTML = response; 
    
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
        str += `< href="restaurant/`+ restaurant['slug']+`">View Details</a>`;
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
    str +=`<form onsubmit = "`
    str+= response['function']
    str +=`"><input type="submit" value = "`
    str += response['newText']
    str+= `"/></form>`
    str+= `<h1>A TEST</h1>`
    document.getElementById('add-or-remove').innerHTML = str;
}

function removeFavoriteFromDashboard(restaurant_slug){
    const stringURL = 'remove/?slug=' + restaurant_slug
    ajaxGetRequest(stringURL, dashboardCallBack)
}

function dashboardCallBack(response) {
    let str = "";	
    str += String();
    // document.getElementById("restaurant-list").innerHTML = response; 
    
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
        str += `<a href="{% url "djangoeats:restaurant_detail" restaurant.slug %}">View Details</a>`;
        str+= `<input type="button" class="favourite-action" value="Remove from Favorites" onclick="removeFavoriteFromDashboard('{{ restaurant.slug }}')"/>`;
        str += `</div>`;
        }
    }
    document.getElementById("restaurant-list").innerHTML = str; 
}



//Code I found online
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
