
from geopy.geocoders import Nominatim
from flask import session
geolocator = Nominatim(user_agent="YoCompro")

def set_location(latitude, longitude):
    location = geolocator.reverse(f"{latitude}, {longitude}")
    city = location.raw["address"]["city"]
    session['city'] = city
    session['lat'] = latitude
    session['lon'] = longitude
    return location

def asked_location(bool):
    session['location_requested'] = bool