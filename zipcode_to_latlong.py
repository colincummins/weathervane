def zipcode_to_latlong(zipcode):
    #Takes a zipcode and returns a latitude and longitude
    import wv_config
    
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent=wv_config.user_agent)
    location = geolocator.geocode(zipcode)
    return location.latitude,location.longitude