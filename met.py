#!/usr/bin/python
from urllib2 import urlopen 
from xml.etree.ElementTree import parse
import sys
import datetime

www=False
sta="LEMD"
stareq =  sys.argv[1:]
if stareq : 
    sta = stareq[0].upper()                             # requested a station
    if len(stareq) >1 and stareq[1] == 'www':
	www=True
	print 'WWW'
else:
    sta = "LEMD" 
    www=False 
print "Meteo in ... ", sta

url=('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=25' % sta)
f = urlopen(url)
doc = parse(f)
	
obs= list(doc.iterfind('data/METAR'))
i = len(obs) - 1
while i >= 0:
	item=obs[i]
	i -=1
	rawtext			=item.findtext('raw_text')
	station			=item.findtext('station_id')
	obstime			=item.findtext('observation_time')
	temp			=item.findtext('temp_c')
	dewp   			=item.findtext('dewpoint_c')
	winddir   		=item.findtext('wind_dir_degrees')
	windspeed   		=item.findtext('wind_speed_kt')
	windgust   		=item.findtext('wind_gust_kt')
	visibility	 	=item.findtext('visibility_statute_mi')
	if visibility == None: visibility=6.6
	qnh   			=item.findtext('altim_in_hg')
	fc   			=item.findtext('flight_category')
	wx   			=item.findtext('wx_string')
	if wx == None: wx=''
	cloud=''
	for sc in item.findall('sky_condition'):
		scover=sc.get('sky_cover')
		clbase=sc.get('cloud_base_ft_agl')
		cltype=sc.get('cloud_type')
		cloud+=' '+str(scover)
		if clbase != None: cloud +=' at '+str(clbase)
		if cltype != None: cloud +='/'+str(cltype)
	print station, ("%-75s" % rawtext), obstime, cloud, 'Temp:', temp, 'DewP:', dewp, 'Wind Dir.', winddir, 'Wind Speed:', windspeed, 'Wind Gust:', windgust,'Visibility:', visibility, 'QHN:', qnh, fc, wx

f.close()

