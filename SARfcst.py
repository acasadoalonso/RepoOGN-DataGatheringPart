#!/usr/bin/python3
import sys
import urllib.request, urllib.error, urllib.parse
import datetime
import xml.etree.ElementTree as ET
import socket

extend = False
www = False
sta = "LEMD"
stareq = sys.argv[1:]
if stareq:
    sta = stareq[0].upper()                             # requested a station
    if len(stareq) > 1 and stareq[1] == 'www':
        www = True
        print('WWW')
else:
    sta = "LEMD"
    www = False

hostname = socket.gethostname()
print("Meteo in ... ", sta, hostname)

numr=0
url = ('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=1' % sta)
url = ('https://aviationweather.gov/cgi-bin/data/dataserver.php?requestType=retrieve&dataSource=tafs&stationString=%s&hoursBeforeNow=1&format=xml' % sta)
f = urllib.request.urlopen(url)
xml_string = f.read()
#print ("XML:", xml_string)
root = ET.fromstring(xml_string)
# for child in root:
#    print child.tag, child.attrib
for data in root.findall('data'):
    numr = data.get('num_results')
    print("Number of results:", numr)
fc = list(root.iterfind('data/TAF'))
for taf in fc:
    rawtext = taf.findtext('raw_text')
    print(rawtext)
    xdata = list(taf.iterfind('forecast'))
    for fcst in xdata:
        tf = fcst.findtext('fcst_time_from')[11:16]+'Z'
        tt = fcst.findtext('fcst_time_to')[11:16]+'Z'
        ci = fcst.findtext('change_indicator')
        if ci == None:
            ci = ''
        pb = fcst.findtext('probability')
        if pb == None:
            pb = ''
        else:
            pb = pb+'%'
        wx = fcst.findtext('wx_string')
        if wx == None:
            wx = ''
        winddir = fcst.findtext('wind_dir_degrees')
        if winddir == None:
            winddir = ''
        windspeed = fcst.findtext('wind_speed_kt')
        if windspeed == None:
            windspeed = ''
        windgust = fcst.findtext('wind_gust_kt')
        if windgust == None:
            windgust = ''
        visibility = fcst.findtext('visibility_statute_mi')
        if visibility == None:
            visibility = 6.21
        cloud = ''
        for sc in fcst.findall('sky_condition'):
            scover = sc.get('sky_cover')
            clbase = sc.get('cloud_base_ft_agl')
            cltype = sc.get('cloud_type')
            cloud += ' '+str(scover)
            if clbase != None:
                cloud += ' at '+str(clbase)
            if cltype != None:
                cloud += '/'+str(cltype)

        print('From:', tf, 'Until:', tt, ci, pb, cloud, 'Winddir:', winddir, 'WindSpeed:', windspeed, 'WindGust:', windgust, 'Visibility:', visibility, wx)
        cloud = ' '
    if rawtext[4:8] == sta:
        break
f.close()
