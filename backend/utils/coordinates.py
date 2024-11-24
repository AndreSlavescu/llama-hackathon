from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="NestQuest")

def get_coordinates(address: str):
    location = geolocator.geocode(address)

    if location:
        return location.longitude, location.latitude
    return None