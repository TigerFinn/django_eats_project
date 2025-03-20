//Basic search functionality

function searchRestaurants() {	
    //Get inputs
    const nameQuery = document.getElementById('search-name-input').value;
    const addressQuery = document.getElementById('search-address-input').value;
    const cuisineQuery = document.getElementById('search-cuisine-input').value;

    //If no input is made, cancel search
    if (nameQuery == "" && addressQuery == "" && cuisineQuery ==""){
        return;
    }
    
    var	xhttp = new	XMLHttpRequest();	

    //code that would be needed if a post method is used
    // const csrftoken = getCookie('csrftoken');

    //Action listener for xhr change
    xhttp.onreadystatechange = function()	{	
        if	(this.readyState ==	4 && this.status == 200)	{
            //For each restaurant returned by the query, create the html object
            let str = "";	
            response = JSON.parse(this.responseText);
            str += String();
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
                str += `<a href="restaurant/`+ restaurant['slug']+`">View Details</a>`;
                str += `</div>`;
                }
            }
            document.getElementById("restaurant-list").innerHTML = str; 
        }
    };	    

    var searchURL = "search/?name=" + nameQuery + "&address=" + addressQuery + "&cuisine=" + cuisineQuery;
    xhttp.open("GET",searchURL, true);
   
    xhttp.send();	
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
