import urllib2
import json
import datetime
extend = False
f = urllib2.urlopen('http://api.geonames.org/weatherIcaoJSON?ICAO=LEMD&username=acasado')
json_string = f.read()
parsed_json = json.loads(json_string)
observation= parsed_json['weatherObservation']['observation']
print "Meteo in Madrid: " , observation, "UTC Date:", datetime.datetime.utcnow()
otime   = parsed_json['weatherObservation']['datetime']
temp_c  = parsed_json['weatherObservation']['temperature']
dewp    = parsed_json['weatherObservation']['dewPoint']
humit   = parsed_json['weatherObservation']['humidity']
pressure= parsed_json['weatherObservation']['hectoPascAltimeter']
sta     = parsed_json['weatherObservation']['stationName']
print "Data: ", sta, otime, "Temp:", temp_c, "DewP;", dewp, "Humidity:", humit, "% QNH:", pressure
if extend:
    windspe= parsed_json['weatherObservation']['windSpeed']
    winddir= parsed_json['weatherObservation']['windDirection']
 
    print "Data: ", otime, "Wind dir:", winddir, "Wind speed", windspe
f.close()
