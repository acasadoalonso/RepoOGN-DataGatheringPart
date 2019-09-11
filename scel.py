#!/usr/bin/python3

from urllib.request import urlopen
import datetime

from xml.etree.ElementTree import parse
extend = False
import sqlite3
datapath = "/nfs/OGN/DIRdata/"
print("Meteo in Santiago... ")
sta = "SCEL"

conn = sqlite3.connect(datapath+'METEO.db')
curs = conn.cursor()

crecmd = "create table IF NOT EXISTS METEO (date char(6), time char (6), metstation char(4), rowdata TEXT NULL DEFAULT NULL, temp REAL, dewp REAL, winddir int, windspeed int, windgust int, visibility int, qnh REAL, cloud TEXT, fcat TEXT, wxstring TEXT)"
curs.execute(crecmd)
crecmd = "create unique index IF NOT EXISTS METEOIDX on METEO ( date , time, metstation)"
curs.execute(crecmd)

url = ('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=SCEL&hoursBeforeNow=1')
f = urlopen(url)
root = parse(f)

for data in root.findall('data'):
    numr = data.get('num_results')
    print("Number of results:", numr)

obs = list(root.iterfind('data/METAR'))

item = obs[0]

rawtext = item.findtext('raw_text')
station = item.findtext('station_id')
dtetext = item.findtext('observation_time')
date = dtetext[2:4]+dtetext[5:7]+dtetext[8:10]
time = dtetext[11:13]+dtetext[14:16]+dtetext[17:19]
temp = item.findtext('temp_c')
dewp = item.findtext('dewpoint_c')
winddir = item.findtext('wind_dir_degrees')
windspeed = item.findtext('wind_speed_kt')
windgust = item.findtext('wind_gust_kt')
visibility = item.findtext('visibility_statute_mi')
if visibility == None:
    visibility = 6.6
qnh = item.findtext('altim_in_hg')
fc = item.findtext('flight_category')
wx = item.findtext('wx_string')
if wx == None:
    wx = ''
cloud = ''
for sc in item.findall('sky_condition'):
    scover = sc.get('sky_cover')
    clbase = sc.get('cloud_base_ft_agl')
    cltype = sc.get('cloud_type')
    cloud += ' '+str(scover)
    if clbase != None:
        cloud += ' at '+str(clbase)
    if cltype != None:
        cloud += '/'+str(cltype)
print(rawtext)
print(dtetext, "UTC Date/Time now is:", datetime.datetime.utcnow(), date, time)

print(station, cloud, 'Temp:', temp, 'DewP:', dewp, 'Wind Dir.', winddir, 'Wind Speed:', windspeed, 'Wind Gust:', windgust, 'Visibility:', visibility, 'QHN:', qnh, fc, wx)

f.close()


try:
    addcmd = "insert into METEO values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    curs.execute(addcmd, (date, time, station, rawtext, temp, dewp,
                          winddir, windspeed, windgust, visibility, qnh, cloud, fc, wx))

except:
    pass
conn.commit()
conn.close()
