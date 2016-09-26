#!/usr/bin/python
# -*- coding: UTF-8 -*-
MySQL=False
#
# DBdump V2.1
#

def fixcoding(addr):
	if addr != None:
		addr=addr.replace(u'á', u'a')
		addr=addr.replace(u'à', u'a')
		addr=addr.replace(u'â', u'a')
		addr=addr.replace(u'Á', u'A')
		addr=addr.replace(u'é', u'e')
		addr=addr.replace(u'è', u'e')
		addr=addr.replace(u'ê', u'e')
		addr=addr.replace(u'É', u'E')
		addr=addr.replace(u'í', u'i')
		addr=addr.replace(u'ì', u'i')
		addr=addr.replace(u'î', u'i')
		addr=addr.replace(u'Í', u'I')
		addr=addr.replace(u'ó', u'o')
		addr=addr.replace(u'ò', u'o')
		addr=addr.replace(u'ô', u'o')
		addr=addr.replace(u'Ó', u'O')
		addr=addr.replace(u'Ò', u'O')
		addr=addr.replace(u'ú', u'u')
		addr=addr.replace(u'ù', u'u')
		addr=addr.replace(u'û', u'u')
		addr=addr.replace(u'Ú', u'U')
		addr=addr.replace(u'ü', u'u')
		addr=addr.replace(u'ñ', u'n')
		addr=addr.replace(u'Ñ', u'N')
	return addr

#
# Dump the OGN database
#

import sqlite3
import MySQLdb
import datetime 
import time
import sys
import os
import socket
from   geopy.distance  import vincenty      # use the Vincenty algorithm
from   geopy.geocoders import GeoNames      # use the Nominatim as the geolocator
from   geopy.geocoders import Nominatim
import logging
import logging.config

maxdist=300.0
fid=  {'NONE  ' : 0}                        # FLARM ID list
numID=0					    # number of flrams found
fsta= {'NONE  ' : 'NONE  '}                 # STATION ID list

fsloc={'NONE  ' : 0}                        # station location
fsmax={'NONE  ' : 0.0}                      # maximun coverage
fsdis={'NONE  ' : 0.0}                      # distance accumulated
fmaxd={'NONE  ' : 0.0}                      # distance
fmaxlong={'NONE  ' : 0.0}                   # max alt longitude
fmaxlati={'NONE  ' : 0.0}                   # max alt latitude
fmaxalti={'NONE  ' : 0.0}                   # max altitude of that glider

fsabsmax = {}

fmaxdist = 0				    # absolute max distance
fmaxalt  = 0				    # absolute maximun altitude

ndays=0
tmaxa = 0                                   # maximun altitude for the day
tmaxt = 0                                   # time at max altitude
tmid  = ' '                                 # glider ID obtaining max altitude

mlong=0.0
mlati=0.0
tmsta = ''   
cin=0
cpar=0
tpar=0
dtar=False
idr=False
lnames=False
pdte=' '
reg=' '
db=(r'OGN.db')
mydb="OGNDB"
host="ubuntu"
inittime=datetime.datetime.now()
#
# Dump the OGN database
#

print "Dump OGN database V1.1"
print "======================"
dtareq =  sys.argv[1:]

if dtareq and dtareq[0] == 'DATA':
    dtar = True                             # request the data
    idr = False 
elif dtareq and dtareq[0] == 'ID':
    idr = True                              # request the ID
    dtar = False
elif dtareq and dtareq[0] == 'LNAMES':
    lnames = True                              # request the locator names
    dtar = False
elif dtareq and dtareq[0] == 'DATAID':
    dtar = True                             # request the both
    idr = True
elif dtareq and dtareq[0] == 'MYSQL':
    MySQL = True 
    idr = False 
    dtar = False                            # do not request the data/ID
    print "MySQL db:", mydb, host
else:
    dtar = False                            # do not request the data/ID
    idr = False 

# ---------------------------------------------------------- #
logging.basicConfig(filename='.DBdump.log',level=logging.INFO)
logging.info('%30s Dumping the OGN database User=%s at %s', datetime.datetime.now(), os.environ['USER'], socket.gethostname())
if (MySQL):
	logging.info('%30s Opening the MySQL database %s on %s', datetime.datetime.now(), mydb, host)
	conn=MySQLdb.connect(host=host, user="ogn", passwd="ogn", db=mydb)
else:
	logging.info('%30s Opening the SQLite3 database %s ', datetime.datetime.now(), db)
	conn=sqlite3.connect(db)

curs =conn.cursor()
curs2=conn.cursor()
# ---------------------------------------------------------- #
logging.info('%30s Dump stations: ', datetime.datetime.now())
curs.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs.description]
print "STATIONS==>", colnames 

logging.info('%30s Dump station with names: ', datetime.datetime.now())
if (MySQL):
	curs.execute ('select date, idsta, (select descri from RECEIVERS where idsta = idrec), mdist, malt from STATIONS')
else:
	curs.execute ('select date, idsta, (select descri from RECEIVERS where idsta = idrec), mdist, malt from STATIONS')
for row in curs.fetchall():
    print ("%s %-9s %-30s %6.2f %4d" % row)
    
logging.info('%30s Dump receivers: ', datetime.datetime.now())
curs.execute('select * from RECEIVERS')
colnames = [desc[0] for desc in curs.description]
print "RECEIVERS==>", colnames 
curs.execute ('select * from RECEIVERS')
for row in curs.fetchall():
    print row
conn.commit()


logging.info('%30s Dump Gliders: ', datetime.datetime.now())
#
curs.execute('select * from GLIDERS')
colnames = [desc[0] for desc in curs.description]
print "GLIDERS==>", colnames 
curs.execute ('select * from GLIDERS')

row=curs.fetchone()
print row
if idr :
	while True:
		row=curs.fetchone()
		if not row: break
		print row

logging.info('%30s Dump OGNdata0: ', datetime.datetime.now())
if (not MySQL):
	curs.execute('select * from OGNDATA')
	colnames = [desc[0] for desc in curs.description]
	print "OGNDATA==>", colnames 
	conn.commit()

	logging.info('%30s Dump OGNdata1: ', datetime.datetime.now())
	curs.execute ('select * from OGNDATA')

	if dtar:
    		while True:
			row=curs.fetchone()
			if not row: break
			print row
	
logging.info('%30s Dump OGNdata2: ', datetime.datetime.now())
geolocator = Nominatim(timeout=15)
curs.execute ('select idflarm,date,time, station, altitude, distance , latitude, longitude from OGNDATA')
while True:
    rows=curs.fetchmany()
    if not rows: break
    for (ID, dte, tme, sta, alt, dist, lati, long) in rows:
	if pdte != ' ' and pdte != dte:
	    if (MySQL):
	    	cmd="select registration from GLIDERS where idglider = '" + tmid + "'"
	    	curs2.execute(cmd)
	    else:
	    	curs2.execute("select registration from GLIDERS where idglider = ?", [tmid])
	    reg=curs2.fetchone()
	    if reg and reg != None:
		regi=reg
	    else:
		regi=''
	    if lnames and mlati != 0.0 and mlong != 0.0:
		loc = geolocator.reverse([mlati,mlong])
		addr=loc.address
		# print addr
		addr=fixcoding(addr).encode('utf8')
		addr=str(addr) 
		msg= ("Date: %6s Max Alt: %05d m. MSL at %s UTC by: %6s %14s Under: %9s At: %s" % (pdte, tmaxa, tmaxt, tmid, regi, tmsta, addr))
	    else:
		msg= ("Date: %6s Max Alt: %05d m. MSL at %2s:%2s:%2sZ by: %6s %14s Under: %9s " % (pdte, tmaxa, tmaxt[0:2], tmaxt[2:4], tmaxt[4:6], tmid, regi, tmsta))
	    print msg
	    tmaxa=0
	    tmaxt=tme
	    tmid=ID
	    tmsta=sta
	    cpar=0
	    mlati=0.0
	    mlong=0.0
	    ndays+=1
	pdte=dte
	if idr:
	    print ID, dte, tme, sta, alt, dist
	if not ID in fid:
	    fid[ID]=0
	    fsdis[ID]=0.0
	    fsta[ID]=sta
	    fmaxd[ID]=0.0 
	    fmaxalti[ID]=0.0 
	    numID +=1
	fid[ID] +=1
	if dist < maxdist:
		fsdis[ID] +=dist
	if dist > fmaxd[ID] and dist < maxdist:
		fmaxd[ID]=dist
	if dist > fmaxdist and dist < maxdist:
		  fmaxdist=dist
	if alt > fmaxalti[ID]:
		fmaxalti[ID]=alt
		fmaxlong[ID]=long
		fmaxlati[ID]=lati
	if alt > fmaxalt:
                 fmaxalt=alt
	if not sta in fsloc:
	    fsloc[sta]=0
	fsloc[sta] +=1
	if sta in fsmax:
	    if dist < maxdist and dist > fsmax[sta]:
		fsmax[sta]=dist
	else:
	    fsmax[sta]=dist
	if alt > tmaxa:
		    tmaxa = alt                 # maximum altitude for the day
		    tmaxt = tme                 # and time
		    tmid  = ID                  # who did it
		    tmsta = sta                 # station capturing the max altitude
		    tpar=cin
		    mlong=long
		    mlati=lati
	if sta in fsabsmax:
		if alt > fsabsmax[sta]['alti']:
			 fsabsmax[sta]['alti']=alt
			 fsabsmax[sta]['long']=long
			 fsabsmax[sta]['lati']=lati
			 fsabsmax[sta]['date']=dte
			 
	else:
		fsabsmax[sta]=dict(alti= alt, long=long, lati=lati, date=dte)
		
	cin +=1                                 # one more record read
	cpar +=1
	
if cin == 0:
	print "No receords read ..."
	conn.close()
	exit(1)

logging.info('%30s Dump OGNdata3: ', datetime.datetime.now())

if lnames and mlati != 0.0 and mlong != 0.0:
	loc = geolocator.reverse([mlati,mlong])
	addr=loc.address
	addr=fixcoding(addr).encode('utf8')
	addr=str(addr) 
	if reg and reg != None:
		regi=reg
	else:
		regi=''
	msg= ("Date: %6s Max Alt: %05d m. MSL at %s UTC by: %9s %14s Under: %6s At: %s" % (pdte, tmaxa, tmaxt, tmid, regi, tmsta, addr))
else:
	msg= ("Date: %6s Max Alt: %05d m. MSL at %2s:%2s:%2sZ by: %9s %14s Under: %s " % (pdte, tmaxa, tmaxt[0:2], tmaxt[2:4], tmaxt[4:6], tmid, reg, tmsta))
print msg

logging.info('%30s Reports: ', datetime.datetime.now())
#
# reports
#

print 'Input records: ',cin
print "ID   REG    => Base       Record counter    average distance Max Distance"
print "========================================================================="
k=list(fid.keys())                          # list the IDs for debugging purposes
k.sort()                                    # sort the list
	
for key in k:                               # report data
    if key == None:
	continue
    if (MySQL):
    	cmd="select registration from GLIDERS where idglider = '"+ key+"'"
    	curs.execute(cmd)
    else:           
    	curs.execute("select registration from GLIDERS where idglider = ?", [key])
    reg=curs.fetchone()
    mlati=fmaxlati[key]
    mlong=fmaxlong[key]
    if mlati == 0.0 and mlong == 0.0:
	continue
    if lnames and mlati != 0.0 and mlong != 0.0:
	loc = geolocator.reverse([mlati,mlong])
	addr=loc.address
	if addr != None:
		addr=fixcoding(addr).encode('utf8')
		addr=str(addr) 
    else:
	addr= ''
    try:
	msg=("ID: %6s Reg: %-13s ==> Station base: %9s Number of hits: %6d %6.2f Max. distance: %6.2f Max. altitude %4d at: %s" % (key, reg, fsta[key], fid[key], fsdis[key]/fid[key], fmaxd[key], fmaxalti[key], addr))
	print  msg
    except:
	logging.error('%30s error at geolocate coordenates: %9.6f %9.6f %s %s', datetime.datetime.now(), mlati, mlong, key, reg)
	msg=("ID: %6s Reg: %-13s <== Station base: %6s Number of hits: %6d Max. distance: %6.2f Max. altitude %4d at: ??? %9.6f %9.6f " % (key, reg, fsta[key], fid[key], fmaxd[key], fmaxalti[key], mlati, mlong))
	print  msg

print "Number of Flarms found: ", numID
print "STATION ==> Maximun distance and records received "
print "=================================================="
k=list(fsloc.keys())                        # list the receiving stations
k.sort()                                    # sort the list
for key in k:                               # report data distances
    if fsmax[key] > 0:                      # only if we have measured distances
	    addr=' '
	    if lnames:
		mlati=fsabsmax[key]['lati']
		mlong=fsabsmax[key]['long']
		loc = geolocator.reverse([mlati,mlong])
		addr=loc.address
		if addr != None:
			addr=fixcoding(addr).encode('utf8')
			addr=str(addr)
			#print addr
			msg = "%9s ==> %7.2f Kms. achieved and %8d packets received. Max. Alt.: %5.2f  on: %6s at: %50s " % (key,  fsmax[key],  fsloc[key], fsabsmax[key]['alti'], fsabsmax[key]['date'], addr)
	    else:
		    msg = "%9s ==> %7.2f Kms. achieved and %8d packets received. %5.2f %5.2f %5.2f " % (key,  fsmax[key],  fsloc[key], fsabsmax[key]['lati'], fsabsmax[key]['long'], fsabsmax[key]['alti'])
	    print msg

print "Nrecs:", cin, "Number IDs:", len(fid), "Number Sta.:", len(fsmax), "Number days:", ndays, "abs. max altitude:", fmaxalt, "Abs. max distance:", fmaxdist


conn.close()
logging.info('%30s Finish: %30s ', datetime.datetime.now(), datetime.datetime.now() - inittime)

