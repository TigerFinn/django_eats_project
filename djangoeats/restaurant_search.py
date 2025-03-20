from djangoeats.models import Restaurant

#Search terms is list of 4 terms
# ["name","location","cuisine","rating"]
def query_restaurants(search_terms):
    restaurants = list(Restaurant.objects.values())
    results = []
    name = search_terms[0]
    address = search_terms[1]
    cuisine = search_terms[2]

    for restaurant in restaurants:
        if (basicSearch(restaurant['name'],name) and basicSearch(restaurant['address'],address) and basicSearch(restaurant['cuisine'], cuisine)):
            results.append(restaurant)

    return results


def basicSearch(string, searchTerm):
    if searchTerm.lower().strip() in string.lower().strip():
        return True
    return False

    
