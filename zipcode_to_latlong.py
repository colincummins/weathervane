import wv_config
from geopy.geocoders import Nominatim


def zipcode_to_latlong(zipcode):
    # Takes a zipcode and returns a latitude and longitude
    nominatim_query = {
        "postalcode": zipcode[:5],
        "country": "us"
    }
    geolocator = Nominatim(user_agent=wv_config.user_agent)
    location = geolocator.geocode(query=nominatim_query)
    return location.latitude, location.longitude


if __name__ == "__main__":
    print(zipcode_to_latlong('97210-2551'))
