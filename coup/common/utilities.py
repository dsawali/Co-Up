import math

def haversine(lat1,\
              lng1,\
              lat2,\
              lng2):
    """
    Computes the distance in kilometers 
    between two coordinates specified
    in latitude/longitude.

    Formula:
        a = sin²(Δlat/2) + cos lat1 ⋅ cos lat2 ⋅ sin²(Δlng/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = earthRadius ⋅ c
    """
    earthRadius = 6371
    lat1 = math.radians(lat1)
    lng1 = math.radians(lng1)
    lat2 = math.radians(lat2)
    lng3 = math.radians(lng2)

    lat_d = lat2 - lat1
    lng_d = lng2 - lng1   
 

    a = math.sin(lat_d/2)*math.sin(lat_d/2) +\
        math.cos(lat1) * math.cos(lat2) *\
        math.sin(lng_d/2)*math.sin(lng_d/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return earthRadius * c    

       
