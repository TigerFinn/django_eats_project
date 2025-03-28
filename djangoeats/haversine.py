import math

## code i found on the internet for calculating the distance between two co ordinates. 
### https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/ March 2025

def haversine(lat1, lon1, lat2, lon2):
     
  
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 

    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c