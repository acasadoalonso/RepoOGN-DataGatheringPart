
print("Nominatim \n\n")
from geopy.geocoders import Nominatim
Nominatim(user_agent="Repoogn")
geolocator = Nominatim(user_agent="Repoogn", timeout=10)
#loc=geolocator.geocode("Lillo Toledo", exactly_one=True)
#print loc.latitude, loc.longitude, loc.altitude
#loc= geolocator.reverse("39.7168999,-3.32056 ", exactly_one=True)
loc= geolocator.reverse("42.432333,1.903833 ", exactly_one=True)
print((loc.address).encode('utf8'), loc.altitude)
print((loc.address).encode('latin1'), loc.altitude)
print("Google \n\n")

from geopy.geocoders import GoogleV3
geo= GoogleV3(scheme="http", api_key="AIzaSyCKOPCAqnZW-OZvw3hzOjcKTldrZZN9wLo")
#loc=geo.geocode("Lillo Toledo", exactly_one=True)
#print loc.latitude, loc.longitude, loc.altitude
#location = geo.reverse("39.7168999,-3.32056 ", exactly_one=True)
location = geo.reverse("42.432333,1.903833 ", exactly_one=True)
print((location.address).encode('utf8'), location.altitude)
print((location.address).encode('latin1'), location.altitude)
