from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("38.5895, -3.5475")
print(location.address)
lati=40.931
long=-4.2708
location = geolocator.reverse([lati, long])
print(location.address)

