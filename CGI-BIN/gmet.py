#!/usr/bin/python
import cgi
import os
import sys
import cgitb
import urllib2

from xml.etree.ElementTree import parse, fromstring
import sys
import datetime


#html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station are: </H1> <HR> <P> %s </P> </HR> """
html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station (%s) are: </H1> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center></html>"""

www=True
streq =  sys.argv[1:]
if streq :
    	sta = streq[0]                          # request the station
	sta=sta.upper()
	sta=sta.strip()
else:
    	sta = "LEMD"                            # take it as default
        print "Maddrid (LEMD) by default ..."

if www: print (html1 % sta)
if www: print html2
################

url=('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=25' % sta)
f = urllib2.urlopen(url)
doc = parse(f)
	
for data in doc.findall('data'):
    numr = data.get('num_results')
    print "<a> <H1>METAR</H1> Number of results:", numr, "</a></br>"
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
	visibility              =item.findtext('visibility_statute_mi')
        if visibility == None: visibility=6.6
        qnh                     =item.findtext('altim_in_hg')
        fc                      =item.findtext('flight_category')
        wx                      =item.findtext('wx_string')
        if wx == None: wx=''
        cloud=''
        for sc in item.findall('sky_condition'):
                scover=sc.get('sky_cover')
                clbase=sc.get('cloud_base_ft_agl')
                cltype=sc.get('cloud_type')
                cloud+=' '+str(scover)
                if clbase != None: cloud +=' at '+str(clbase)
                if cltype != None: cloud +='/'+str(cltype)

	print "<a>", rawtext, "</a>"
	print "<a>", station, obstime, cloud, 'Temp:', temp, 'DewP:', dewp, 'Wind Dir.', winddir, 'Wind Speed:', windspeed, 'Wind Gust:', windgust,'Visibility:', visibility, 'QHN:', qnh, fc, wx,"</a></br>"

f.close()

################

url =('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=25' % sta)
f = urllib2.urlopen(url)
root = parse(f)
for data in root.findall('data'):
    numr = data.get('num_results')
    print "<a> <H1>TAFOR</H1> Number of results:", numr, "</a>"
fc = list(root.iterfind('data/TAF'))
for taf in fc:
    rawtext=taf.findtext('raw_text')
    print '</br><a>', rawtext, '</a>' 
    xdata=list(taf.iterfind('forecast'))
    for fcst in xdata:
        tf=fcst.findtext('fcst_time_from')[11:16]+'Z'
        tt=fcst.findtext('fcst_time_to')[11:16]+'Z'
        ci=fcst.findtext('change_indicator')
        if ci == None:
                ci=''
        pb=fcst.findtext('probability')
        if pb == None:
                pb=''
        else:
                pb=pb+'%'
        wx=fcst.findtext('wx_string')
        if wx == None:
                wx=''
        winddir=fcst.findtext('wind_dir_degrees')
        if winddir == None:
                winddir=''
        windspeed=fcst.findtext('wind_speed_kt')
        if windspeed == None:
                windspeed=''
        visibility=fcst.findtext('visibility_statute_mi')
        if visibility == None:
                visibility=6.21
	cloud=''
        for sc in fcst.findall('sky_condition'):
                scover=sc.get('sky_cover')
                clbase=sc.get('cloud_base_ft_agl')
                cltype=sc.get('cloud_type')
                cloud+=' '+str(scover)
                if clbase != None: cloud +=' at '+str(clbase)
                if cltype != None: cloud +='/'+str(cltype)
        print '<a> From:',tf, 'Until:', tt, ci, pb, cloud, 'Winddir:', winddir, 'WindSpeed:', windspeed, 'Visibility:', visibility, wx, '</a>'
f.close()
################
if www: print html3
