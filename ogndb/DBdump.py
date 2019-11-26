#!/usr/bin/python3
import config
# -*- coding: UTF-8 -*-
MySQL = False
#
# DBdump V3.0
#


def fixcoding(addr):
    if addr != None:
        addr = addr.replace('á', 'a')
        addr = addr.replace('à', 'a')
        addr = addr.replace('â', 'a')
        addr = addr.replace('Á', 'A')
        addr = addr.replace('é', 'e')
        addr = addr.replace('è', 'e')
        addr = addr.replace('ê', 'e')
        addr = addr.replace('É', 'E')
        addr = addr.replace('í', 'i')
        addr = addr.replace('ì', 'i')
        addr = addr.replace('î', 'i')
        addr = addr.replace('Í', 'I')
        addr = addr.replace('ó', 'o')
        addr = addr.replace('ò', 'o')
        addr = addr.replace('ô', 'o')
        addr = addr.replace('Ó', 'O')
        addr = addr.replace('Ò', 'O')
        addr = addr.replace('ú', 'u')
        addr = addr.replace('ù', 'u')
        addr = addr.replace('û', 'u')
        addr = addr.replace('Ú', 'U')
        addr = addr.replace('ü', 'u')
        addr = addr.replace('ñ', 'n')
        addr = addr.replace('Ñ', 'N')
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
from tqdm import tqdm
from geopy.distance import vincenty         # use the Vincenty algorithm
from geopy.geocoders import GeoNames        # use the Nominatim as the geolocator
from geopy.geocoders import Nominatim
Nominatim(user_agent="Repoogn")
geolocator = Nominatim(user_agent="Repoogn")
import logging
import logging.config

maxdist = 300.0
fid = {'NONE  ': 0}                         # FLARM ID list
numID = 0				    # number of flrams found
fsta = {'NONE  ': 'NONE  '}                 # STATION ID list

fsloc = {'NONE  ': 0}                       # station location
fsmax = {'NONE  ': 0.0}                     # maximun coverage
fsdis = {'NONE  ': 0.0}                     # distance accumulated
fmaxd = {'NONE  ': 0.0}                     # distance
fmaxlong = {'NONE  ': 0.0}                  # max alt longitude
fmaxlati = {'NONE  ': 0.0}                  # max alt latitude
fmaxalti = {'NONE  ': 0.0}                  # max altitude of that glider

fsabsmax = {}

fmaxdist = 0				    # absolute max distance
fmaxalt = 0				    # absolute maximun altitude

ndays = 0
tmaxa = 0                                   # maximun altitude for the day
tmaxt = 0                                   # time at max altitude
tmid = ' '                                  # glider ID obtaining max altitude

mlong = 0.0
mlati = 0.0
tmsta = ''
cin = 0
cpar = 0
tpar = 0
dtar = False
idr = False
lnames = False
pdte = ' '
reg = ' '
mydb = config.DBname
host = config.DBhost
DBuser = config.DBuser
DBpasswd = config.DBpasswd
DBpath = config.DBpath
db = DBpath+(config.SQLite3)
inittime = datetime.datetime.now()
#
# Dump the OGN database
#

print("Dump OGN database V3.0")
print("======================")
dtareq = sys.argv[1:]

if dtareq and dtareq[0] == 'DATA':
    dtar = True                             # request the data
    idr = False
elif dtareq and dtareq[0] == 'ID':
    idr = True                              # request the ID
    dtar = False
elif dtareq and dtareq[0] == 'LNAMES':
    lnames = True                           # request the locator names
    dtar = False
elif dtareq and dtareq[0] == 'DATAID':
    dtar = True                             # request the both
    idr = True
elif dtareq and dtareq[0] == 'MYSQL':
    MySQL = True
    idr = False
    dtar = False                            # do not request the data/ID
    print("MySQL db:", mydb, " at ", host)
else:
    dtar = False                            # do not request the data/ID
    idr = False

# print (dtareq, dtareq[0], "MySQL", MySQL, "dtar", dtar, "LNAMES", lnames, "IDR", idr)
# ---------------------------------------------------------- #
logging.basicConfig(filename='.DBdump.log', level=logging.INFO)
logging.info('%30s Dumping the OGN database User=%s at %s',
             datetime.datetime.now(), os.environ['USER'], socket.gethostname())
if (MySQL):
    logging.info('%30s Opening the MySQL database %s on %s',
                 datetime.datetime.now(), mydb, host)
    conn = MySQLdb.connect(host=host, user=DBuser, passwd=DBpasswd, db=mydb)
else:
    logging.info('%30s Opening the SQLite3 database %s ',
                 datetime.datetime.now(), db)
    conn = sqlite3.connect(db)

curs  = conn.cursor()
curs2 = conn.cursor()
# ---------------------------------------------------------- #
logging.info('%30s Dump stations: ', datetime.datetime.now())
curs.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs.description]
print(("STATIONS==>", colnames))

logging.info('%30s Dump station with names: ', datetime.datetime.now())
if (MySQL):
    curs.execute('select date, idsta, (select descri from RECEIVERS where idsta = idrec), mdist, malt from STATIONS')
else:
    curs.execute('select date, idsta, (select descri from RECEIVERS where idsta = idrec), mdist, malt from STATIONS')
for row in curs.fetchall():
    print(("%s %-9s %-30s %6.2f %4d" % row))

logging.info('%30s Dump receivers: ', datetime.datetime.now())
curs.execute('select * from RECEIVERS')
colnames = [desc[0] for desc in curs.description]
print(("RECEIVERS==>", colnames))
curs.execute('select * from RECEIVERS')
for row in curs.fetchall():
    print(row)
conn.commit()


logging.info('%30s Dump Gliders: ', datetime.datetime.now())
#
curs.execute('select * from GLIDERS')
colnames = [desc[0] for desc in curs.description]
print(("GLIDERS==>", colnames))
curs.execute('select * from GLIDERS')
row = curs.fetchone()
print(row)
if idr:
    while True:
        row = curs.fetchone()
        if not row:
            break
        print(row)

logging.info('%30s Dump OGNdata0: ', datetime.datetime.now())
if (not MySQL):
    curs.execute('select * from OGNDATA')
    colnames = [desc[0] for desc in curs.description]
    print(("OGNDATA==>", colnames))
    conn.commit()

    logging.info('%30s Dump OGNdata1: ', datetime.datetime.now())
    curs.execute('select * from OGNDATA')

    if dtar:
        while True:
            row = curs.fetchone()
            if not row:
                break
            print(row)

logging.info('%30s Dump OGNdata2: ', datetime.datetime.now())
geolocator = Nominatim(user_agent="Repoogn", timeout=15)
curs.execute('select count(*) from OGNDATA')
row = curs.fetchone()
nrecs=row[0]
print("Number of records on OGNDATA:", nrecs)
curs.execute('select idflarm,date,time, station, altitude, distance , latitude, longitude from OGNDATA limit 1000000')
offset=1000000
while True:
    rows = curs.fetchmany()
    if not rows:
             if offset > nrecs:
                break
             else:
                curs.execute('select idflarm,date,time, station, altitude, distance , latitude, longitude from OGNDATA limit '+str(offset)+' , 1000000')
                offset+=1000000
                continue
    for (ID, dte, tme, sta, alt, dist, lati, longi) in rows:
        if pdte != ' ' and pdte != dte:
            if (MySQL):
                cmd = "select registration from GLIDERS where idglider = '" + tmid + "'"
                curs2.execute(cmd)
            else:
                curs2.execute(
                    "select registration from GLIDERS where idglider = ?", [tmid])
            reg = curs2.fetchone()
            if reg and reg != None:
                regi = reg
            else:
                regi = ''
            if lnames and mlati != 0.0 and mlong != 0.0:
                loc = geolocator.reverse([mlati, mlong])
                addr = loc.address
                # print addr
                if addr != None:
                    addr = fixcoding(addr).encode('utf8')
                    addr = str(addr)
                    msg = ("Date: %6s Max Alt: %05d m. MSL at %s UTC by: %6s %14s Under: %9s At: %s" % (
                    pdte, tmaxa, tmaxt, tmid, regi, tmsta, addr))
                else:
                    msg = "Not a valid GeoLocation address ..."
            else:
                msg = ("Date: %6s Max Alt: %05d m. MSL at %2s:%2s:%2sZ by: %6s %14s Under: %9s " % (
                    pdte, tmaxa, tmaxt[0:2], tmaxt[2:4], tmaxt[4:6], tmid, regi, tmsta))
            print(msg)
            tmaxa = 0
            tmaxt = tme
            if len(ID) == 9:
                tmid = ID[3:9]
            else:
                tmid = ID
            tmsta = sta
            cpar = 0
            mlati = 0.0
            mlong = 0.0
            ndays += 1
        pdte = dte
        if idr:
            print((ID, dte, tme, sta, alt, dist))
        if not ID in fid:
            fid[ID] = 0
            fsdis[ID] = 0.0
            fsta[ID] = sta
            fmaxd[ID] = 0.0
            fmaxalti[ID] = 0.0
            numID += 1
        fid[ID] += 1
        if dist < maxdist:
            fsdis[ID] += dist
        if dist > fmaxd[ID] and dist < maxdist:
            fmaxd[ID] = dist
        if dist > fmaxdist and dist < maxdist:
            fmaxdist = dist
        if alt > fmaxalti[ID]:
            fmaxalti[ID] = alt
            fmaxlong[ID] = longi
            fmaxlati[ID] = lati
        if alt > fmaxalt:
            fmaxalt = alt
        if not sta in fsloc:
            fsloc[sta] = 0
        fsloc[sta] += 1
        if sta in fsmax:
            if dist < maxdist and dist > fsmax[sta]:
                fsmax[sta] = dist
        else:
            fsmax[sta] = dist
        if alt > tmaxa:
            tmaxa = alt                 # maximum altitude for the day
            tmaxt = tme                 # and time
            tmid = ID                   # who did it
            tmsta = sta                 # station capturing the max altitude
            tpar = cin
            mlong = longi
            mlati = lati
        if sta in fsabsmax:
            if alt > fsabsmax[sta]['alti']:
                fsabsmax[sta]['alti'] = alt
                fsabsmax[sta]['longi'] = longi
                fsabsmax[sta]['lati'] = lati
                fsabsmax[sta]['date'] = dte

        else:
            fsabsmax[sta] = dict(alti=alt, longi=longi, lati=lati, date=dte)

        cin += 1                                 # one more record read
        cpar += 1

if cin == 0:
    print("No receords read ...")
    conn.close()
    exit(1)

logging.info('%30s Dump OGNdata3: ', datetime.datetime.now())

if lnames and mlati != 0.0 and mlong != 0.0:
    loc = geolocator.reverse([mlati, mlong])
    addr = loc.address
    addr = fixcoding(addr).encode('utf8')
    addr = str(addr)
    if reg and reg != None:
        regi = reg
    else:
        regi = ''
    msg = ("Date: %6s Max Alt: %05d m. MSL at %s UTC by: %9s %14s Under: %6s At: %s" % (
        pdte, tmaxa, tmaxt, tmid, regi, tmsta, addr))
else:
    msg = ("Date: %6s Max Alt: %05d m. MSL at %2s:%2s:%2sZ by: %9s %14s Under: %s " % (
        pdte, tmaxa, tmaxt[0:2], tmaxt[2:4], tmaxt[4:6], tmid, reg, tmsta))
print(msg)

logging.info('%30s Reports: ', datetime.datetime.now())
#
# reports
#

print('Input records: ', cin)
print("ID   REG    => Base       Record counter    average distance Max Distance")
print("=========================================================================")
# list the IDs for debugging purposes
k = list(fid.keys())
k.sort()                                    # sort the list

for key in k:                               # report data
    if key == None:
        continue
    if len(key) == 9:
        gkey = key[3:9]
    else:
        gkey = key
    if (MySQL):
        cmd = "select registration from GLIDERS where idglider = '" + gkey+"'"
        curs.execute(cmd)
    else:
        curs.execute(
            "select registration from GLIDERS where idglider = ?", [gkey])

    reg = curs.fetchone()
    try:

        mlati = fmaxlati[key]
        mlong = fmaxlong[key]
    except:
        continue
    if mlati == 0.0 and mlong == 0.0:
        continue
    if lnames and mlati != 0.0 and mlong != 0.0:
        loc = geolocator.reverse([mlati, mlong])
        addr = loc.address
        if addr != None:
            addr = fixcoding(addr).encode('utf8')
            addr = str(addr)
    else:
        addr = ''
    try:
        msg = ("ID: %6s Reg: %-13s ==> Station base: %9s Number of hits: %6d %6.2f Max. distance: %6.2f Max. altitude %4d at: %s" %
               (key, reg, fsta[key], fid[key], fsdis[key]/fid[key], fmaxd[key], fmaxalti[key], addr))
        print(msg)
    except:
        logging.error('%30s error at geolocate coordenates: %9.6f %9.6f %s %s',
                      datetime.datetime.now(), mlati, mlong, key, reg)
        msg = ("ID: %6s Reg: %-13s <== Station base: %6s Number of hits: %6d Max. distance: %6.2f Max. altitude %4d at: ??? %9.6f %9.6f " %
               (key, reg, fsta[key], fid[key], fmaxd[key], fmaxalti[key], mlati, mlong))
        print(msg)

print(("Number of Flarms found: ", numID))
print("STATION ==> Maximun distance and records received ")
print("==================================================")
k = list(fsloc.keys())                      # list the receiving stations
k.sort()                                    # sort the list
for key in k:                               # report data distances
    if fsmax[key] > 0:                      # only if we have measured distances
        addr = ' '
        if lnames:
            mlati = fsabsmax[key]['lati']
            mlong = fsabsmax[key]['longi']
            loc = geolocator.reverse([mlati, mlong])
            addr = loc.address
            if addr != None:
                addr = fixcoding(addr).encode('utf8')
                addr = str(addr)
                #print addr
                msg = "%9s ==> %7.2f Kms. achieved and %8d packets received. Max. Alt.: %5.2f  on: %6s at: %50s " % (
                    key,  fsmax[key],  fsloc[key], fsabsmax[key]['alti'], fsabsmax[key]['date'], addr)
        else:
            msg = "%9s ==> %7.2f Kms. achieved and %8d packets received. %5.2f %5.2f %5.2f " % (
                key,  fsmax[key],  fsloc[key], fsabsmax[key]['lati'], fsabsmax[key]['longi'], fsabsmax[key]['alti'])
        print(msg)

print(("Nrecs:", cin, "Number IDs:", len(fid), "Number Sta.:", len(
    fsmax), "Number days:", ndays, "abs. max altitude:", fmaxalt, "Abs. max distance:", fmaxdist))


conn.close()
logging.info('%30s Finish: %30s ', datetime.datetime.now(),
             datetime.datetime.now() - inittime)
