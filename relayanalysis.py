#!/usr/bin/python
import time
import sys
import os
from   datetime import datetime, timedelta
from   geopy.distance import vincenty       # use the Vincenty algorithm
import MySQLdb                              # the SQL data base routines
import sqlite3                              # the SQL data base routines
import kglid
import argparse

print "Start RELAY analysis"
print "===================="
maxdist=0.0
totdist=0.0
ncount=0
nrecs=0
fid=  {'NONE  ' : 0}                        # FLARM ID list
import config                               # import the main settings
DBname=config.DBname
DBhost=config.DBhost
DBuser=config.DBuser
DBpasswd=config.DBpasswd
MySQL=config.MySQL
fn=sys.argv[1:]                                 # take the name of the second arg
fname=str(fn)[2:16]
dte=str(fn)[6:12]                               # take the date from the file name
date=datetime.now()                         # get the date

parser=argparse.ArgumentParser(description="OGN Tracker relay analysis")
parser.add_argument('-g', '--glider',    required=True, dest='glider',   action='store')
parser.add_argument('-t', '--towplane',  required=True, dest='towplane', action='store')
parser.add_argument('-o', '--ogntrcker', required=True, dest='ogntracker', action='store')
parser.add_argument("-n", '--name',      required=True, dest='filename', action='store')
parser.add_argument('-i', '--intval',    required=False, dest='intval', action='store', default='10')
args=parser.parse_args()
glid=args.glider
tow= args.towplane
ogntracker=args.ogntracker
fname=args.filename
intsec=int(args.intval)
dte=fname[4:10]                         # take the date from the file name
print "Glider:", args.glider, "Tow plane:", args.towplane, "OGN tracker:", args.ogntracker, kglid.kglid[ogntracker[3:9]],"Filename:", args.filename, "Interval:", args.intval


if (MySQL):
        conn=MySQLdb.connect(host=DBhost, user=DBuser, passwd=DBpasswd, db=DBname)     # connect with the database
else:
        conn=sqlite3.connect(r'OGN.db')     # connect with the database
curs1=conn.cursor()                          # set the cursor
curs2=conn.cursor()                          # set the cursora

print 'File name:', fname, "at", dte, 'Process date/time:', date.strftime(" %y-%m-%d %H:%M:%S")     # display file name and time
datafilei = open(fname, 'r')                # open the file with the logged data

lasttime=''
while True:                                 # until end of file
        data=datafilei.readline()               # read one line
        if not data:                            # end of file ???
                break
        nrecs += 1
        relpos= data.find("APRS,RELAY*")
        if relpos == -1:
                continue
        flrmid=data[0:9]
        dtepos=data.find(":/")+2
        timefix=data[dtepos:dtepos+6]
        sta=data[relpos+16:dtepos-2]
        if timefix == lasttime:
                continue
        lasttime=timefix
        if flrmid[3:9] in kglid.kglid:     # if it is a known glider ???
                        r=kglid.kglid[flrmid[3:9]]     # get the registration
        else:
                        r='NOREG '                  # no registration
        if r == glid or r == tow:
                continue
        inter=timedelta(seconds=intsec)
        Y=int(dte[0:2]) + 2000
        M=int(dte[2:4])
        D=int(dte[4:6])
        h=int(timefix[0:2])
        m=int(timefix[2:4])
        s=int(timefix[4:6])
        T=datetime(Y,M,D,h,m,s)
        T1=T-inter
        T2=T+inter
        timefix1=T1.strftime("%H%M%S")
        timefix2=T2.strftime("%H%M%S")
        sql1="select latitude, longitude from OGNDATA where idflarm ='"+ogntracker+"' and date = '"+dte+"' and time>='"+timefix1+"' and time <='"+timefix2+"';"
        sql2="select latitude, longitude from OGNDATA where idflarm ='"+flrmid+"'     and date = '"+dte+"' and time= '"+timefix+"';"
        #print nrecs, timefix, flrmid
        curs2.execute(sql2)
        row2=curs2.fetchone()
        if (row2) != None:
                latlon2=(row2[0], row2[1])
                curs1.execute(sql1)
                rows1=curs1.fetchall()
                nr=0
                maxrr=0
                for row1 in rows1:
                        nr +=1
                        maxrr=0
                        latlon1=(row1[0], row1[1])
                        distance=vincenty(latlon1, latlon2).km
                        distance=round(distance,3)
                        if distance > maxdist:
                                maxdist=distance
                        if distance > maxrr and distance > 0.050:
                                maxrr=distance
                        else:
                                continue
                        if not flrmid in fid :                      # if we did not see the FLARM ID
                                fid[flrmid]=maxrr
                        if fid[flrmid]<maxrr:
                                fid[flrmid]=maxrr
                totdist += maxrr
                if maxrr > 0:
                        ncount += 1
                        print "N:", ncount, nr, "\t\t ID:", r, flrmid, "Max. dist.:", maxrr, "Kms. at:",timefix, sta

print "Max. distance", maxdist, "Avg. distance", totdist/ncount, "Total number of records", nrecs
print fid
k=list(fid.keys())                  # list the IDs for debugging purposes
k.sort()                            # sort the list
for key in k:                       # report data
        if key[3:9] in kglid.kglid:
                gid=kglid.kglid[key[3:9]]    # report the station name
        else:
                gid="NOSTA"             # marked as no sta
        print key, '=>', gid, fid[key]

datafilei.close()                           # close the input file
conn.close()                                # Close libfap.py to avoid memory leak

