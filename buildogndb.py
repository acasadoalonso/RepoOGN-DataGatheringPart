#!/usr/bin/python
#
# This program reads the the records received from the OGN APRS server for SPAIN
# and generates the OGN database
# It runs 30 minutes after the sunset in Lillo(TO) - LELT
#
# Author: Angel Casado - August 2015
#
import datetime 
import time
import sys
import os
import kglid                                # import the list on known gliders
import config                               # import the main settings
from   libfap import *                      # the packet parsing function 
from   parserfuncs import *                 # the ogn/ham parser functions 
from   geopy.distance import vincenty       # use the Vincenty algorithm
from   geopy.geocoders import GeoNames      # use the Nominatim as the geolocator
import sqlite3                              # the SQL data base routines
import MySQLdb                              # the SQL data base routines

#
# ---------- main code ---------------
#

fid=  {'NONE  ' : 0}                        # FLARM ID list
fsta= {'NONE  ' : 'NONE  '}                 # STATION ID list
ftkot={'NONE  ' : 0}                        # take off time
flndt={'NONE  ' : 0}                        # take off time
fsloc={'NONE  ' : (0.0, 0.0)}               # station location
fslla={'NONE  ' : 0.0}			    # station latitude
fsllo={'NONE  ' : 0.0}			    # station longitude
fslal={'NONE  ' : 0.0}			    # station altitude
fsmax={'NONE  ' : 0.0}                      # maximun coverage
fsalt={'NONE  ' : 0}                        # maximun altitude
ftkok={datetime.datetime.utcnow(): 'NONE  '}  # Take off time 
tmaxa = 0                                   # maximun altitude for the day
tmaxt = 0                                   # time at max altitude
tmid  = 0                                   # glider ID obtaining max altitude
tmsta = ''
prt=False
MySQL=False
DBname=config.DBname
DBhost=config.DBhost
DBuser=config.DBuser
DBpasswd=config.DBpasswd
blacklist = ['FLR5B0041']                   # blacklist



print "Start build OGN database V1.10"
print "=============================="
dtereq =  sys.argv[1:]
if dtereq and dtereq[0] == 'date':
    dter = True                             # request the date
else:
    dter = False                            # do not request the date
if dtereq and dtereq[0] == 'name':
    nmer = True                             # request the name
    #prt=True
    prt=False
elif dtereq and dtereq[0] == 'MYSQL':
    nmer = True                             # request the name
    prt=False
    MySQL=True
    print "MySQL DB :", DBname, "User:", DBuser,"@", DBhost 
else:
    nmer = False                            # do not request the name
    
cin  = 0                                    # input record counter
cout = 0                                    # output file counter
date=datetime.datetime.now()                # get the date
dte=date.strftime("%y%m%d")                 # today's date
fname='DATA'+dte+'.log'                     # file name from logging

#fname='DATA150722.log'                     # example of file name 

if not dter and not nmer:                   # check if we need to request date
    print 'User: ', os.environ['USER']      # tell that
    fname='DATA'+dte+'.log'                 # build the file name with today's date
elif nmer:
    fn=sys.argv[2:]                         # take the name of the second arg
    fname=str(fn)[2:16]
    dte=str(fn)[6:12]                       # take the date from the file name
else:
    dte=raw_input('Enter date:')            # otherwise ask for the date
    if dte == '':                           # if no input 
        dte=date.strftime("%y%m%d")         # use the default
    fname='DATA'+dte+'.log'                 # build the file name with the date entered
    
print 'File name:', fname, 'Process date/time:', date.strftime(" %y-%m-%d %H:%M:%S")     # display file name and time

geolocator=GeoNames(country_bias='Spain', username='acasado' )
datafilei = open(fname, 'r')                # open the file with the logged data
if (MySQL):
	conn=MySQLdb.connect(host=DBhost, user=DBuser, passwd=DBpasswd, db=DBname)     # connect with the database
else:
	conn=sqlite3.connect(r'OGN.db')     # connect with the database
curs=conn.cursor()                          # set the cursor
 
print "libfap_init"
libfap.fap_init()
nrec=0

while True:                                 # until end of file 
    data=datafilei.readline()               # read one line
    if not data:                            # end of file ???
                                            # report the findings and close the files
        print '===> Input records: ',dte, cin, 'Ouput files:',cout # report number of records read and files generated
        k=list(fid.keys())                  # list the IDs for debugging purposes
        k.sort()                            # sort the list
        
        for key in k:                       # report data
            if key[3:9] in kglid.kglid:     # if it is a known glider ???
                r=kglid.kglid[key[3:9]]     # get the registration
            else:
                r='NOREG '                  # no registration
            ttime=0                         # flying time 
            if ftkot[key] != 0  and flndt[key] != 0: 
                ttime = flndt[key] - ftkot[key]
            else:
                ttime = ' '
            if flndt[key]  != 0 :
                ltime=flndt[key]
            else:
                ltime = ' '
            if prt:
                print key, '=>', 'Base:', fsta[key], 'Reg:', r, 'Take off:', ftkot[key], 'Landing:', ltime, ttime, 'Nrecs:', fid[key]
                                            # report FLARM ID, station used,  record counter, registration, take off time and landing timecd ../..
            
 
        k=list(ftkok.keys())                # list the takes off times
        k.sort()                            # sort the list
        for to in k:                        # report by take off time
                key= ftkok[to]
                if key[3:9] in kglid.kglid: # if it is a known glider ???
                    r=kglid.kglid[key[3:9]] # get the registration
                else:
                    r='Noreg '              # no registration
                ttime=0                     # flying time 
                if ftkot[key] != 0  and flndt[key] != 0:  # if both
                    ttime = flndt[key] - ftkot[key]
                else:
                    ttime= ' '
                if flndt[key]  != 0 :
                    ltime=flndt[key]
                else:
                    ltime = ' '
                if prt:
                    print to, ':::>', key, fsta[key], r, ftkot[key], ltime, ttime
                
        k=list(fsloc.keys())                # list the receiving stations
        k.sort()                            # sort the list
        for key in k:                       # report data distances
            if fsmax[key] > 0:              # only if we have measured distances
                if prt:
                    print key, '==>', fsmax[key], ' Kms. '      # distance
		if (MySQL):
                	addcmd="insert into STATIONS values ('" + key + "','" + dte + "'," + str(fsmax[key]) +  "," + str(fsalt[key]) + ")"
                	curs.execute(addcmd)
		else:
                	addcmd="insert into STATIONS values (?,?,?,?)"
                	curs.execute(addcmd, (key, dte, fsmax[key], fsalt[key]))
	#
	    if (MySQL):
            	selcmd="select idrec from RECEIVERS where idrec='" + key +"'"  # SQL command to execute: SELECT
            	curs.execute(selcmd)
	    else:
            	selcmd="select idrec from RECEIVERS where idrec=?"  # SQL command to execute: SELECT
            	curs.execute(selcmd, (key,))
            if curs.fetchone() == None:
		gid='Noreg '                # for unknown receiver
        	if spanishsta(key) or frenchsta(key):
            		if key in kglid.kglid:
                		gid=kglid.kglid[key]        # report the station name
            		else:
                		gid="NOSTA"                 # marked as no sta
		lati=fslla[key]             # latitude
        	long=fsllo[key]             # longitude
        	alti=fslal[key]             # altitude

		if key != "None" and key != None:
                	if prt:
                    		print key, 'Adding ==>', gid, lati, long, alti
			if (MySQL):
                		addcmd="insert into RECEIVERS values ('" + key + "','" + gid + "'," + str(lati)+  "," + str(long)+ "," + str(alti)+ ")"
                		curs.execute(addcmd)
			else:
                		inscmd="insert into RECEIVERS values (?, ?, ?, ?, ?)"
                		curs.execute(inscmd, (key, gid, lati, long, alti))
	#
        conn.commit()
        break                               # work done

    if len(data) < 40:                      # that is the case of end of file when the ognES.py process is still
        continue                            # nothing else to do
#   ready to handle a record
    nrec += 1
    ix=data.find('>')
    cc= data[0:ix]
    cc=cc.upper()
    data=cc+data[ix:]

    packet       = libfap.fap_parseaprs(data, len(data), 0) # parser the information
    longitude    = get_longitude(packet)
    latitude     = get_latitude(packet)
    altitude     = get_altitude(packet)
    speed        = get_speed(packet)
    course       = get_course(packet)
    path         = get_path(packet)
    ptype        = get_type(packet)
    dst_callsign = get_dst_callsign(packet)
    destination  = get_destination(packet)
    header       = get_header(packet)
    otime        = get_otime(packet)
    dist=0
 
    callsign=packet[0].src_callsign         # get the call sign FLARM ID
    if (data.find('TCPIP*') != -1):         # ignore the APRS lines
        id=callsign                         # station ID
        if not id in fsloc :
            fsloc[id]=(latitude, longitude) # save the loction of the station
	    fslla[id]=latitude
	    fsllo[id]=longitude
	    fslal[id]=altitude
            fsmax[id]=0.0                   # initial coverage zero
            fsalt[id]=0                     # initial coverage zero
        continue                            # go for the next record
    if cc in blacklist:
        continue
    id=data[0:9]                            # the flarm ID/ICA/OGN 
    idname=data[3:9]                        # exclude the FLR part
    scolon=data.find(':')                   # find the colon
    station=data[data.find('qAS')+4:scolon] # the station name is after the qAS, 
    station=station.upper()                 # translate to uppercase
    if path=='RELAY*':
        print "RELAY:", id, ":::", station , longitude, latitude, altitude, speed, course, ptype, otime, "DATA:", data
    if spanishsta(station):                 # only Spanish stations
        if not id in fid :                  # if we did not see the FLARM ID
            fid  [id]=0                     # init the counter
            fsta [id]=station               # init the station receiver
            ftkot[id]=0                     # take off time/ initial seeing  - null for the time being
            flndt[id]=0                     # landing  time - null for the time being
            cout += 1                       # one more file to create
            
        fid[id] +=1                         # increase the number of records read
        p1=data.find(':/')+2                # scan for the body of the APRS message
        hora=data[p1:p1+6]                  # get the GPS time in UTC
        long=data[p1+7:p1+11]+data[p1+12:p1+14]+'0'+data[p1+14]         # get the longitude
        lati=data[p1+16:p1+21]+data[p1+22:p1+24]+'0'+data[p1+24]        # get the latitude
        p2=data.find('/A=')+3               # scan for the altitude on the body of the message
        altif=data[p2+1:p2+6]               # get the altitude in feet
	if  data[p2+7] == '!':              # get the unique id
                uniqueid     = data[p2+13:p2+23] # get the unique id
                extpos       = data[p2+7:p2+12] # get extended position indicator
        else:
                uniqueid     = data[p2+7:p2+17] # get the unique id
                extpos=' '
        p3=data.find('fpm')                 # scan for the rate of climb
        roclimb      = data[p3-3:p3]        # get the rate of climb
        p4=data.find('rot')                 # scan for the rate of climb
        rot      = data[p4-3:p4]            # get the rate of turn
        p5=data.find('dB')                  # scan for the sensitivity
        sensitivity = data[p5-4:p5]         # get the sensitivity
        p6=data.find('gps')                 # scan for gps info
        gps      = data[p6:p6+6]            # get the gps
        altim=altitude                      # the altitude in meters
        if altim > 15000 or altim < 0:
            altim=0
        alti='%05d' % altim                 # convert it to an string
         
 
        if speed > 50 and ftkot[id] == 0:   # if we do not have the take off time ??
                ftkot[id] = otime           # store the take off time
                ftkok[otime]=id             # list by take off time 
        if speed < 20 and speed > 5 and ftkot[id] != 0:   # if we do not have the take off time ??
                flndt[id] = otime           # store the landing time
        if station in fsloc:                # if we have the station yet
                distance=vincenty((latitude, longitude), fsloc[station]).km    # distance to the station
                dist=distance
                if distance > 250.0:
                    print ">>Distcheck: ", distance,"Nrec:", nrec,  data
                elif distance > fsmax[station]: # if higher distance
                    fsmax[station]=distance     # save the new distance
                if altim > fsalt[station]:  # if higher altitude
                    fsalt[station]=altim    # save the new altitude
        if altim > tmaxa:
                tmaxa = altim               # maximum altitude for the day
                tmaxt = hora                # and time
                tmid  = id                  # who did it
                tmsta = station             # station capturing the max altitude
        if uniqueid[0:2] != "id":	    # check for a valid uniqueid
		continue
	# write the DB record
	if (MySQL):
        	addcmd="insert into OGNDATA values ('" +idname+ "','" + dte+ "','" + hora+ "','" + station+ "'," + str(latitude)+ "," + str(longitude)+ "," + str(altim)+ "," + str(speed)+ "," + str(course)+ "," + str(roclimb)+ "," +str( rot) + "," +str(sensitivity)
        	addcmd=addcmd+",'" + gps+ "','" + uniqueid+ "'," + str(dist)+ ",'" + extpos+ "')"
		try:
			curs.execute(addcmd) 
		except:
			print ">>>MySQL error:", nrec, cin, addcmd
	else:
        	addcmd="insert into OGNDATA values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        	curs.execute(addcmd, (idname, dte, hora, station, latitude, longitude, altim, speed, course, roclimb, rot,sensitivity, gps, uniqueid, dist, extpos))
        cin +=1                             # one more record read
        
# -----------------  final process ----------------------

datafilei.close()                           # close the input file
datef=datetime.datetime.now()               # get the time & date
conn.commit()
conn.close()                                # Close libfap.py to avoid memory leak
libfap.fap_cleanup()


if tmid[3:9] in kglid.kglid:                # if it is a known glider ???
    gid=kglid.kglid[tmid[3:9]]              # report the registration
else:
    gid=tmid    
print "Maximun altitude for the day:", tmaxa, ' meters MSL at:', tmaxt, 'Z by:', gid, 'Station:', tmsta
print 'Bye ...: Stored', cin," records of ", nrec,' read. Time and Time used:', datef, datef-date      # report the processing time

    
