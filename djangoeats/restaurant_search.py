from djangoeats.models import Restaurant

#Search terms is list of 4 terms
# ["name","location","cuisine","rating"]
def query_restaurants(search_terms):
    restaurants = list(Restaurant.objects.values())
    results = []
    name = search_terms[0]
    address = search_terms[1]
    cuisine = search_terms[2]
    # rating = search_terms[3]
    for restaurant in restaurants:
        if (basicSearch(restaurant['name'],name) and basicSearch(restaurant['address'],address) and basicSearch(restaurant['cuisine'], cuisine)):
            results.append(restaurant)

    return results


def basicSearch(string, searchTerm):
    if searchTerm.lower().strip() in string.lower().strip():
        return True
    return False


#Functionality doesn't work because terminal won't recognise the import
def main():
    name = input("Search by name: ")
    location = input("Search by location: ")
    cuisine = input("Search by cuisine:")
    try:
        rating = int(input("Search by rating: "))
    except TypeError:
        print("Valid rating not given, search rating set to 0")
    results = query_restaurants([name, location, cuisine])
    for result in results:
        print(result.name)


if __name__ == "__main__":
    main()