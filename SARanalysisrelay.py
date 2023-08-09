#!/usr/bin/python3
import time
import sys
import os
from datetime import datetime, timedelta
from geopy.distance import geodesic	    # use the Vincenty algorithm
import MySQLdb                              # the SQL data base routines
import sqlite3                              # the SQL data base routines
from ognddbfuncs import *		    # import the DDB functions
import argparse
from tqdm import tqdm
sys.path.insert(0, '/nfs/OGN/src/funcs')
from parserfuncs import *                   # the ogn/ham parser functions
import subprocess

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

#
# ----------------------------------------------------------------------------
#

def printfid(fid, key):		            # print the list of relays
    for k in fid[key]:
        for kk in k:
            if getognchk(kk[3:9]):
                gid = getognreg(kk[3:9])    # report the registration
            else:
                gid = "NOSTA"               # marked as no sta
            print(gid, k[kk], ';', end=' ')
    return (';')
#
# ----------------------------------------------------------------------------
#


def sa_builddb(fname, schema_file="STD"):   # build a in memory database with all the fixes

    relaycnt = 0                            # counter of relay packages
    relaycntr = 0                           # counter of std relay packages
    relayglider = {}                        # list of relay glider and tracker
    fsour = {}				    # sources
    ogndatasql = "CREATE TABLE OGNDATA (idflarm char(9) , date char(6), time char(6), station char(9), latitude float, longitude float, altitude int, speed float, course int, roclimb int, rot float, sensitivity float, gps char(6), uniqueid char(10), distance float, extpos char (5));"

    trkstatussql = "CREATE TABLE OGNTRKSTATUS ( id varchar(9) NOT NULL, station varchar(9) NOT NULL, otime datetime NOT NULL, status varchar(255) NOT NULL)"

    con = sqlite3.connect(":memory:")	    # SQLITE3 DB
    con.isolation_level = None
    curs = con.cursor()			    # initial cursor
                                            # create the temporary database clone of OGNDB
    if schema_file == "STD":
        try:
            curs.executescript(ogndatasql)
        except Exception as e:
            print("Failed to create temp.db from STD schema, error")
    else:
        fSchema = open(schema_file)
        print("Gen SQLITE3 temp DB:", schema_file, " open ok")
        for line in fSchema.readlines():
            schemaStr = ""
            schemaStr += " %s" % line
            try:
                curs.executescript(schemaStr)
            except Exception as e:
                print("Failed to create temp.db from schema file, error")
        fSchema.close()

    try:
        curs.executescript(trkstatussql)
    except Exception as e:
        print("Failed to create temp.db from TRKSTATUS schema, error")

    con.commit()			    # commit the DB just created, empty
    nlines=file_len(fname)                  # get the number of lines 
    print ("Building the sqlite3 DB using the file: "+fname+" with lines:", nlines)
                                            # open the file with the logged data
    datafilei = open(fname, 'r')
    nrecs = 0
    pbar = tqdm(total=nlines)               # indicate the total number of lines 
    while True:                             # until end of file
        pbar.update(1) 
        data = datafilei.readline()         # read one line
        if not data:                        # end of file ???
                                            # report the findings and close the files
            break
        if len(data) < 40:             	    # that is the case of end of file
            continue                        # nothing else to do
                                            #	ready to handle a record
        ix = data.find('>')		    # translate to uppercase the ID
        cc = data[0:ix]
        cc = cc.upper()
        data = cc+data[ix:]
        msg = {}
        if len(data) > 0 and data[0] != "#":
            msg = parseraprs(data, msg)     # parser the data
            if msg == -1:		    # parser error
                print("Parser error:", data)
                continue
            path = msg['path']
            source = msg['source']          # source of the data OGN/SPOT/SPIDER/...
            if source == 'TTN':
               print(data)
            if path == 'aprs_receiver' or path == 'receiver' or source == 'TTN':
                continue
            if source != 'OGN' and source != 'TTN':
                continue
            ident = msg['id']          	    # id
            if 'aprstype' in msg:
                mtype = msg['aprstype']	    # message type
            else:
                print ("MSG>>>", msg)
            longitude = msg['longitude']
            latitude = msg['latitude']
            altitude = msg['altitude']
            otime = msg['otime']
            source = msg['source']          # source of the data OGN/SPOT/SPIDER/...
            if len(source) > 4:
                source = source[0:3]

            if not source in fsour:	    # did we see this source
                fsour[source] = 1	    # init the counter
            else:
                fsour[source] += 1          # increase the counter

            # if std records
            if 'relay' in msg:
                relay = msg['relay']
            else:
                relay = ''
            if ((path == 'aprs_aircraft' or source == 'TTN') and (relay == 'RELAY' or relay == "OGNDELAY"))  or (path == 'tracker' and relay[0:3] == "OGN"):
                station = msg['station']    # get the station name
                if relay == "RELAY" or relay == "OGNDELAY":
                    relaycntr += 1
                if relay[0:3] == "OGN":	    # if it is a OGN tracker relay msg
                    if not id in relayglider:
                        rr = {} 	    # temp
                        #print "otime", otime.strftime("%y%m%d%H%M%S")
                        rr[path[0:9]] = otime.strftime("%H%M%S")
                        # add the id to the table of relays.
                        relayglider[ident] = rr
                    relaycnt += 1	    # increase the counter
            else:
                station = msg['station']    # get the station name
            if path == 'aprs_receiver':
                continue                    # go for the next record
            if mtype == 'status':           # if status report
                status = msg['status']      # get the status message
                # and the station receiving that status report
                station = msg['station']
                # build the OTIME based on the data
                Y = int(dte[0:2])+2000
                M = int(dte[2:4])
                D = int(dte[4:])
                h = int(status[0:2])
                m = int(status[2:4])
                s = int(status[4:6])
                # date from file name and time from status report
                otime = datetime(Y, M, D, h, m, s)

                if len(status) > 254:
                    status = status[0:254]
                #print "Status report:", id, station, otime, status
                inscmd = "insert into OGNTRKSTATUS values ('%s', '%s', '%s', '%s' )" %\
                    (ident, station, otime, status)
                try:
                    curs.execute(inscmd)
                except MySQLdb.Error as e:
                    try:
                        print(">>>SQL1 Error [%d]: %s" % (e.args[0], e.args[1]))
                    except IndexError:
                        print(">>>SQL2 Error: %s" % str(e))
                    print(">>>SQL3 error:",  cout, inscmd)
                    print(">>>SQL4 data :",  data)
                continue

            ident = data[0:9]               # the flarm ID/ICA/OGN
            idname = data[0:9]              # exclude the FLR part
            if latitude == -1 or longitude == -1 or mtype == 'satus':
                continue
            # and the station receiving that status report
            station = msg['station']
            course = msg['course']
            speed = msg['speed']
            uniqueid = msg['uniqueid']
            if len(uniqueid) > 10:
                uniqueid = uniqueid[0:10]	# in this database only 10 chars
            extpos = msg['extpos']
            roclimb = msg['roclimb']
            rot = msg['rot']
            sensitivity = msg['sensitivity']
            gps = msg['gps']
            hora = msg['time']
            dist = -1				# if we can not get the distance
            altim = altitude                    # the altitude in meters
            if uniqueid[0:2] != "id":	    	# check for a valid uniqueid
                continue
            # write the DB record eithher on MySQL or SQLITE3
            addcmd = "insert into OGNDATA values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            curs.execute(addcmd, (idname, dte, hora, station, latitude, longitude, altim,
                                  speed, course, roclimb, rot, sensitivity, gps, uniqueid, dist, extpos))
            nrecs += 1

    datafilei.close()		# close the input file
    con.commit()   	    	# commit the DB
    pbar.close()                # release the tqdm object
    print("Number of records on the temp DB:", nrecs)
    print("Number of relay packages:", relaycntr, relaycnt)
    print("Sources: ", fsour)

    return con			# just return the connetion ID
#
# ----------------------------------------------------------------------------
#

version='V2.0'
print("Start RELAY analysis "+version)
print("===========================")
maxdist = 0.0
totdist = 0.0
ncount = 0
nrecs = 0
nrecords = 0
relaycnt = 0
lasttime = ''
fid = {}   		                    # FLARM ID list
fn = sys.argv[1:]                           # take the name of the second arg
date = datetime.now()                       # get the date

parser = argparse.ArgumentParser(description="OGN Tracker relay analysis")
parser.add_argument("-n",  '--name',       required=True,
                    dest='filename', action='store')
parser.add_argument('-i',  '--intval',     required=False,
                    dest='intval',   action='store', default='05')
parser.add_argument('-sa', '--standalone', required=False,
                    dest='sa',       action='store', default='NO')
parser.add_argument('-s',  '--schema',     required=False,
                    dest='schema',   action='store', default='STD')
parser.add_argument('-m',  '--mindist',    required=False,
                    dest='mindist',  action='store', default='1.0')
args = parser.parse_args()
fname = args.filename
sa = args.sa
mindist = float(args.mindist)
DBschema = args.schema
intsec = int(args.intval)
# take the date from the file name
dte = fname[-10:-4]
print("Filename:", args.filename, "Interval:", args.intval, "StandAlone:", sa, "DBschema file", DBschema, "Min Dist ", mindist, "Date:", dte)
if (not os.path.isfile(fname)):
    print("File does not exists...")
    exit(1)
if sa == "YES":				    # standalone case ???
    # build the temporary DB on memory and return the connect
    conn1 = sa_builddb(fname, DBschema)
    conn2 = conn1			    # same DB
    MySQL = False			    # do not use SQL in this case
    curs1 = conn1.cursor()           	    # set the cursor
    curs1.execute("select count(*) from OGNDATA;")
    print("OGNDATA records:     ", curs1.fetchone()[0])
    curs1.execute("select count(*) from OGNTRKSTATUS;")
    print("OGNTRKSTATUS records:", curs1.fetchone()[0])
    curs1.execute("select * from OGNTRKSTATUS;")
    rows = curs1.fetchall()
    # for row in rows:
    #print "TRKTRK:", row

else:
    import config                           # import the main settings
    DBname = config.DBname
    DBhost = config.DBhost
    DBuser = config.DBuser
    DBpasswd = config.DBpasswd
    MySQL = config.MySQL
    # connect with the daily database
    conn1 = MySQLdb.connect(host=DBhost, user=DBuser,
                            passwd=DBpasswd, db=DBname)
    # connect with the ogntrkstatus databasea
    try:
       conn2 = MySQLdb.connect(host=DBhost, user=DBuser,
                            passwd=DBpasswd, db='APRSLOG')
    except:
       print ("Error on DB APRSLOG ....")
       exit()

curs1 = conn1.cursor()                 	    # set the cursor
curs2 = conn1.cursor()                	    # set the cursora
curs3 = conn2.cursor()                	    # set the cursora

print('Filename:', fname, "at", dte, 'Process date/time:', date.strftime(
    " %y-%m-%d %H:%M:%S"))     # display file name and time
# open the file with the logged data
datafilei = open(fname, 'r')
while True:                                 # until end of file
    data = datafilei.readline()             # read one line
    nrecords += 1
    if not data:                            # end of file ???
        break
    relpos = data.find(",RELAY*")           # look for old RELAY messages
    if relpos != -1:
        relaycnt += 1		            # just increas the counter and leave
        continue

    # look for the new RELAY message that tell us who the the station making the RELAY
    relpos = data.find("*,qAS")
    if relpos == -1:
        continue		            # nothing to do
    ogntracker = data[relpos-9:relpos]      # OGN tracker doing the RELAY
    if ogntracker[0:3] != "OGN":	    # just be sure that is an OGN tracker ???
        continue
    nrecs += 1			            # increase the counter of RELAY messages
    # device (either flarm or tracker) that has been done the RELAY
    flrmid = data[0:9]
    dtepos = data.find(":/")+2	            # position report
    # OGN station receiving the RELAY message
    station = data[relpos+6:dtepos-2]
    if data[dtepos+6] == 'h':	            # check the time format
        timefix = data[dtepos:dtepos+6]
    elif data[dtepos+6] == 'z':
        timefix = data[dtepos+2:dtepos+6]+'00'
    else:
        continue		            # unkown format ... nothing to do
    if timefix == lasttime:
        continue
    lasttime = timefix
    # scan for the altitude on the body of the message
    p2 = data.find('/A=')+3
    altif = data[p2+1:p2+6]                 # get the altitude in feet
    if altif.isdigit():
        altim = int(int(altif)*0.3048)      # convert the altitude in meters
    else:
        altim = 0
    if altim > 15000 or altim < 0:
        altim = 0
    alti = '%05d' % altim                   # convert it to an string

    if getognchk(flrmid[3:9]):              # if it is a known glider ???
        reg = getognreg(flrmid[3:9])        # get the registration
    else:
        reg = 'NOREG '                      # no registration
    if getognchk(ogntracker[3:9]):          # if it is a known glider ???
        trk = getognreg(ogntracker[3:9])
    else:
        trk = ogntracker	            # no tracker registration
    inter1 = timedelta(seconds=intsec)
    inter2 = timedelta(seconds=60*5)
    Y = int(dte[0:2]) + 2000		    # build the datetime
    M = int(dte[2:4])
    D = int(dte[4:6])
    h = int(timefix[0:2])
    m = int(timefix[2:4])
    s = int(timefix[4:6])
    #print nrecs,  flrmid, ogntracker, data
    # in formate datetime in order to handle the intervals
    T = datetime(Y, M, D, h, m, s)
    T1 = T-inter1			    # +/- interval to look into database
    T2 = T+inter1
    T3 = T-inter2		    	    # +/- interval to look into database
    T4 = T+inter2
    timefix1 = T1.strftime("%H%M%S")	    # now in string format
    timefix2 = T2.strftime("%H%M%S")
    otime1 = T1.strftime("%Y-%m-%d %H:%M:%S")
    otime2 = T2.strftime("%Y-%m-%d %H:%M:%S")
    # build the SQL commands
    sql1 = "select latitude, longitude, altitude from OGNDATA where idflarm ='" + \
        flrmid+"'     and date = '"+dte+"' and time= '"+timefix+"';"
    sql2 = "select latitude, longitude, altitude from OGNDATA where idflarm ='" + \
        ogntracker+"' and date = '"+dte+"' and time>='" + \
        timefix1+"' and time <='"+timefix2+"';"
    sql3 = "select id, station, status from OGNTRKSTATUS where id = '" + \
        ogntracker+"' and otime > '"+otime1+"' and otime < '"+otime2+"';"
    #print ("SSS=>", nrecs, dte, timefix, flrmid, ogntracker,"\n", sql1,"\n", sql2,"\n", sql3, "\n", data)
    curs1.execute(sql1)
    row1 = curs1.fetchone()		    # should be one one record
    #print "R1", row1
    if (row1) != None:			    # should be always one record
        latlon1 = (row1[0], row1[1])        # position of the glider
        # look for all the OGN trackers positions in that interval
        curs2.execute(sql2)
        rows2 = curs2.fetchall()	    # get all position
        nr = 0
        maxrr = 0			    # max distance on this run
        maxalt = 0			    # altitude at that max distance
        for row2 in rows2:		    # scan all the posible records
            nr += 1			    # number of OGN tracker reconds found
            maxrr = 0			    # maximun range
            latlon2 = (row2[0], row2[1])    # position of the OGN tracker
            altitude = row2[2]		    # altitude of the tracker
            # get the distance from the flarm to the tracker
            distance = geodesic(latlon1, latlon2).km
            distance = round(distance, 3)   # round it to 3 decimals
            #print "DDD", flrmid, ogntracker, distance
            if distance > maxdist:	    # maximun absolute distance
                maxdist = distance
            if distance > maxrr and distance > 0.050:  # max distance for this scan
                maxrr = distance
                maxalt = altitude	    # the altitude at that distance
            else:
                continue
        if maxrr > 0:			    # if we found something
            maxrange = {}		    # build the dict
            maxrange[ogntracker] = maxrr    # just the ogn tracker and max dist
            if not flrmid in fid:           # if we did not see the FLARM ID
                maxlist = []		    # init the list
                maxlist.append(maxrange)
                fid[flrmid] = maxlist
            else:
                mm = fid[flrmid]            # the maxlist
                #print "TTT", flrmid, mm
                idx = 0
                found = False
                for entry in mm:
                    if ogntracker in entry:
                        found = True
                        if entry[ogntracker] < maxrr:
                            mm[idx] = maxrange
                            fid[flrmid] = mm
                            break
                    idx += 1

                if not found:		    # if that tracker is not on the list, just add it
                    fid[flrmid].append(maxrange)
            ncount += 1

            curs3.execute(sql3)
            row3 = curs3.fetchall()	    # should be at least one record
            status = ' '
            for row in row3:
                key = row[0]
                if getognchk(key[3:9]):
                    gid = getognreg(key[3:9])    # report the glider reg
                else:
                    gid = "NOSTA"
                status += gid
                status += ' :: '
                status += row[1]
                status += ' :: '
                status += row[2]
                status += ' ::: '
            if status != ' ':
                sta = "OGNTRK Status: "+status
            else:
                sta = ''

            if maxrr > mindist:  # only report in case of more than minimun distance

                print("N:%5d:%3d  OGNTRK: %6s %9s  Alt.: %6.1f <<<>>> FlrmID: %6s %9s Max. dist.: %6.3f Kms. at: %sZ Altitud: %sm. MSL from: %s %s" % (
                    ncount, nr, trk, ogntracker, maxalt, reg, flrmid, maxrr, timefix, alti, station, sta))

        totdist += maxrr		    # add the total distance

if ncount > 0:
    print("\n\nMax. distance", maxdist, "Avg. distance", totdist/ncount)
print("Old relays", relaycnt, "New relays:", nrecs, "Number of records:", nrecords)
#print "\n\n", fid, "\n\n"
k = list(fid.keys())                    # list the IDs for debugging purposes
k.sort()                                # sort the list
for key in k:                           # report data
    if getognchk(key[3:9]):
        gid = getognreg(key[3:9])       # report the glider reg
    else:
        gid = "NOSTA"                   # marked as no sta
    print(key, ':', gid, "==>", printfid(fid, key))

datafilei.close()                       # close the input file
conn1.close()                           # Close the database
conn2.close()                           # Close the database
