#!/usr/bin/python3
#
# gather the WX record from the APRS file and decode it
#

# example:   grep OGNDVS /nfs/OGN/DIRdata/DATA* | grep LEZS | tail -n 20 | python ~/src/APRSsrc/wx.py
#import cgi
import os
import sys
import argparse
import time
import sys
import datetime

from parserfuncs import parseraprs
import fileinput

import ssl
import socket
from dtfuncs import *
ssl.match_hostname = lambda cert, hostname: True

import sqlite3
datapath = "/nfs/OGN/DIRdata/"
hostname = socket.gethostname()
version='V1.0'
date = datetime.now()
print("\n\nWeather gathering from OGN:  "+version)
print("Time:",date )
#					  report the program version based on file date
print("Program Version:", time.ctime(os.path.getmtime(__file__)))
print("============================================")
import git
prt = False
try:
   repo = git.Repo(__file__, search_parent_directories=True)
   sha = repo.head.object.hexsha
except:
   sha='NO SHA'
print ("Git commit info:", sha)
parser = argparse.ArgumentParser(description="OGN Tracker relay analysis")
parser.add_argument("-n",  '--name',       required=False,
                    dest='filename', action='store', default='ALL')
parser.add_argument('-p',  '--print',     required=False,
                    dest='print',   action='store')
args = parser.parse_args()
fname = args.filename
prtt  = args.print
if prtt != None:
   prt = True
else:
   prt = False

print ("Args: FN:", fname, "PRT:", prt, prtt)

msg={}


conn = sqlite3.connect(datapath+'SARMETEO.db')
curs = conn.cursor()

crecmd = "create table IF NOT EXISTS WX (date char(6), time char (6), metstation char(9), rowdata TEXT NULL DEFAULT NULL, wind char(12), temp REAL, humidity REAL, rain char(12));"
curs.execute(crecmd)
crecmd = "create unique index IF NOT EXISTS WXIDX on METEO ( date , time, metstation)"
curs.execute(crecmd)
print ("Table created or connected")
curs.execute("delete from WX;")			# delete all the records ... we plan to add all new
records=0

################
date = datetime.now()
dte = date.strftime("%y%m%d")       # today's date
filename="/nfs/OGN/DIRdata/DATA.active"
#
for line in reversed(list(open(filename))):
    rawtext=line
    parseraprs(line, msg)
    if msg['source'] != 'WTX':
       continue
    #print ("LLL", rawtext)
    metstation = msg['station']
    otime=msg['otime']
    date = otime.strftime("%y%m%d")
    tme = otime.strftime("%H%M%S")
    windspeed=msg['windspeed']
    if windspeed == ' ':
       #print ("WWW", rawtext)
       windspeed ='0/0/0'
    tempf=msg['temp']
    humidity=msg['humidity']
    rain=msg['rain']
    if tempf != ' ' and tempf != 0:
       tempc = round((float(tempf)-32)*5/9, 2)
    else:
       tempc=0.0
    message=""
    if tempc != 0.0:
       message += " Temp: %.2fºC"%tempc
    if humidity != ' ':
       message +=  " Humidity: "+msg['humidity']+"%"
    if rain != ' ':
       message +=  " Rain: "+msg['rain']+" Hourly "
    if prt:
       print ("Station:", msg['station'], "Time (UTC):",date, tme , "Wind (dir/spd/burst):", msg['windspeed'], message)
    try:
       addcmd = "insert into WX values (?,?,?,?,?,?,?,?)"
       curs.execute(addcmd, (date, tme, metstation, rawtext, windspeed, tempc, humidity, rain))
       records += 1
    except sqlite3.Error as er:
       print(er.sqlite_errorcode)  # Prints 275
       print(er.sqlite_errorname)
curs.execute ("select count(*) from WX;")
print  ("WX OGNDATA records:     ", curs.fetchone()[0])
print  ("Total recordds added: ", records, "from:", hostname)
conn.commit()
conn.close()

