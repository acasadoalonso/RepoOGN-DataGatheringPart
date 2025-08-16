#!/usr/bin/python3
#
# gather the WX record from the APRS file, decode it and add it to the SARMETEO database
#

# example:   python SARwx.py 
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
version='V1.1'
date = datetime.now()
print("\n\nWeather gathering from OGN:  "+version)
print("Time:",date )
#					  report the program version based on file date
print("Program Version:", time.ctime(os.path.getmtime(__file__)))
print("============================================")
import platform
print("Python version:", platform.python_version())
import git
prt = False
try:
   repo = git.Repo(__file__, search_parent_directories=True)
   sha = repo.head.object.hexsha
except:
   sha='NO SHA'
print ("Git commit info:", sha)
print("============================================")
parser = argparse.ArgumentParser(description="OGN Add APRS meteo to the DB")
parser.add_argument("-n",  '--name',       required=False,
                    dest='filename', action='store', default='/nfs/OGN/DIRdata/DATA.active')
parser.add_argument('-p',  '--print',     required=False,
                    dest='print',   action='store')
args = parser.parse_args()
fname = args.filename
prtt  = args.print
if prtt != None:
   prt = True
else:
   prt = False

print ("Args: FileName:", fname, "PRT:", prt, prtt)

msg={}


conn = sqlite3.connect(datapath+'SARMETEO.db')
curs = conn.cursor()

crecmd = "create table IF NOT EXISTS WX (date char(6), time char (6), metstation char(9), rowdata TEXT NULL DEFAULT NULL, wind char(12), temp REAL, humidity REAL, rain char(12));"
curs.execute(crecmd)
crecmd = "create unique index IF NOT EXISTS WXIDX on METEO ( date , time, metstation)"
curs.execute(crecmd)
print ("Table created or connected")
curs.execute("delete from WX;")			# delete all the records from WX table ... we plan to add all new
records=0

################
date = datetime.now()
dte = date.strftime("%y%m%d")       # today's date
#filename="/nfs/OGN/DIRdata/DATA.active"
filename=fname
nrecords=0
#
for line in reversed(list(open(filename))):	# read the whole file DATA*.active
    nrecords +=1				# record counter
    rawtext=line				# the raw text
    parseraprs(line, msg)			# parse the line using the python parser
    if msg['source'] != 'WTX':			# if not weather ignore it
       continue
    #print ("LLL", rawtext)
    metstation    = msg['station']
    otime         = msg['otime']
    date          = otime.strftime("%y%m%d")
    tme           = otime.strftime("%H%M%S")
    windspeed     = msg['windspeed']
    tempf         = msg['temp']
    humidity      = msg['humidity']
    rain          = msg['rain']
						# validate the values
    if tempf != ' ' and tempf != 0:
       tempc = round((float(tempf)-32)*5/9, 2)	# convert a Celsius
    else:
       tempc=0.0
    if windspeed == ' ':
       #print ("WWW", rawtext)
       windspeed ='0/0/0'
    message=""					# built the message
    if tempc != 0.0:
       message += " Temp: %.2fºC"%tempc
    if humidity != ' ':
       message +=  " Humidity: "+msg['humidity']+"%"
    if rain != ' ':
       message +=  " Rain: "+msg['rain']+" Hourly "
    if prt:
       print ("Station:", msg['station'], "Time (UTC):",date, tme , "Wind (dir/spd/burst):", msg['windspeed'], message)
    try:					# add it now to the METEO.db
       addcmd = "insert into WX values (?,?,?,?,?,?,?,?)"
       curs.execute(addcmd, (date, tme, metstation, rawtext, windspeed, tempc, humidity, rain))
       records += 1
    except sqlite3.Error as er:
       print(er.sqlite_errorcode)  		# Prints 275
       print(er.sqlite_errorname)

curs.execute ("select count(*) from WX;")	# double check the number of records
print  ("\n\nWX OGNDATA records now:     ", curs.fetchone()[0])
print  ("\nTotal recordds added: ", records, "from ", nrecords, records/nrecords*100, "% total from host:", hostname,"\n\n")
conn.commit()
conn.close()

