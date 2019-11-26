#!/usr/bin/python3
#
# This program reads the the records received from the OGN APRS server for SPAIN
# and generates IGC files for each flight
# It runs 30 minutes after the sunset in Lillo(TO) - LELT
#
# Author: Angel Casado - May 2015
#
import time
import sys
import socket
import config

sys.path.insert(0, '/nfs/OGN/src/funcs')
sys.path.insert(0, '/nfs/OGN/src/SARsrc')
datapath = config.DBpath
#print ("Path:", sys.path)
import os
import kglid                                # import the list on known gliders
from datetime import *                      # the ogn/ham parser functions
from parserfuncs import *                   # the ogn/ham parser functions
from geopy.distance import vincenty         # use the Vincenty algorithm
from geopy.geocoders import GeoNames        # use the Nominatim as the geolocator
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Repoogn", timeout=5)  # create the instance

#
# ---------- main code ---------------
#
pgmver="V2.1"
fid = {'NONE  ': 0}                         # FLARM ID list
fsta = {'NONE  ': 'NONE  '}                 # STATION ID list
ffd = {'NONE  ': None}                      # file descriptor list
ftkot = {'NONE  ': 0}                       # take off time
flndt = {'NONE  ': 0}                       # take off time
fsloc = {'NONE  ': (0.0, 0.0)}              # station location
fsmax = {'NONE  ': 0.0}                     # maximun coverage
fsfix = {'NONE  ': 0}                       # number of fixes
fsour = {}				    # sources
ftkok = {datetime.utcnow(): 'NONE  '}       # Take off time
tfixs = 0                                   # total number of fixes
tmaxa = 0                                   # maximun altitude for the day
tmaxt = 0                                   # time at max altitude
tmid = 0                                    # glider ID obtaining max altitude
tmsta = ''
tmp = ''
mlong = 0.0                                 # longitude on the max altiutde point
mlati = 0.0                                 # latitude of idem
blacklist = ['FLR5B8041']                   # blacklist
www = False
prt = True


#print os.environment
if 'USER' in os.environ:
    user = os.environ['USER']
else:
    user = "www-data"			    # assume www
if 'APACHE_RUN_USER' in os.environ or user == "www-data":        # check if www

    www = True
    prt = False
    tmp = 'tmp/'
else:
    print("===============================")

if prt:
    print("Start process OGN records "+pgmver)
    print("===============================")
    print("User:", user)
dtereq = sys.argv[1:]
if dtereq and dtereq[0] == 'date':
    dter = True                             # request the date
else:
    dter = False                            # do not request the date
if dtereq and dtereq[0] == 'name':
    name = True                             # request the date
else:
    name = False                            # do not request the date
cin = 0                                     # input record counter
cout = 0                                    # output file counter
date = datetime.now()                       # get the date
dte = date.strftime("%y%m%d")               # today's date
fname = 'DATA'+dte+'.log'                   # file name from logging
paths=[]				    # paths used
hostname = socket.gethostname()

# fname='DATA170515.log'                    # example of file name
fn = ''
if not dter:                                # check if we need to request date

    fname = 'DATA'+dte+'.log'               # build the file name with today's date
else:
    dte = input('Enter date:')              # oherwise ask for the date
    if dte == '':                           # if no input
        dte = date.strftime("%y%m%d")       # use the default
                                            # build the file name with the date entered
    fname = 'DATA'+dte+'.log'
if name:
    fn = sys.argv[2:]                       # take the name of the second arg
    fname = str(fn)[2:]
    fname = fname.rstrip("]'")		    # clear garbage
    p = str(fn).find("DATA")		    # look for DATA
                                            # take the date from the file name
    dte = str(fn)[p+4:p+10]
if prt:
    print('File name: ', fn, fname, 'Process date/time:', date.strftime(
        " %y-%m-%d %H:%M:%S"), dte)         # display file name and time

geolocator = GeoNames(country_bias='Spain', username='acasado')
                                            # open the file with the logged data
datafilei = open(datapath+fname, 'r')


while True:                                 # until end of file
    data = datafilei.readline()             # read one line
    if not data:                            # end of file ???
                                            # report the findings and close the files
        if prt:
                                            # report number of records read and files generated
            print('Input records: ', cin, 'Ouput files:', cout)
                                            # list the IDs for debugging purposes
        k = list(fid.keys())
        k.sort()                            # sort the list

        for key in k:                       # report data by flarm id
            if key[3:9] in kglid.kglid:     # if it is a known glider ???
                r = kglid.kglid[key[3:9]]   # get the registration
            else:
                r = 'NOREG '                # no registration
            ttime = 0                       # flying time
            if ftkot[key] != 0 and flndt[key] != 0:
                ttime = flndt[key] - ftkot[key]
            else:
                ttime = ' '
            if flndt[key] != 0:
                ltime = flndt[key]
            else:
                ltime = ' '
            if prt:
                print(key, '=>', 'Base:', fsta[key], 'Reg:', r, 'Take off:', ftkot[
                    key], 'Landing:', ltime, ttime, 'Nrecs:', fid[key])
                # report FLARM ID, station used,  record counter, registration, take off time and landing time
            if ffd[key] != None:
                ffd[key].close()            # and close all the file

        k = list(ftkok.keys())              # list the takes off times
        k.sort()                            # sort the list
        for to in k:                        # report by take off time
            key = ftkok[to]
            if key[3:9] in kglid.kglid:     # if it is a known glider ???
                r = kglid.kglid[key[3:9]]   # get the registration
            else:
                r = 'Noreg '                # no registration
            ttime = 0                       # flying time
            if ftkot[key] != 0 and flndt[key] != 0:  # if both
                ttime = flndt[key] - ftkot[key]
            else:
                ttime = ' '
            if flndt[key] != 0:
                ltime = flndt[key]
            else:
                ltime = ' '
            if prt:
                print(to, ':::>', key, fsta[key], r, ftkot[key], ltime, ttime)

        k = list(fsloc.keys())              # list the receiving stations
        k.sort()                            # sort the list
        for key in k:                       # report data distances
            if fsmax[key] > 0:              # only if we have measured distances
                tfixs += fsfix[key]         # total number of fixes
                if prt:
                                            # distance
                    print(key, '==>', fsmax[key], ' Kms. and number of fixes: ', fsfix[key])
        print(paths)
        # work done, finish the reporting now ...
        break
#--------------------------------------------------------------------------------------------------
    # that is the case of end of file when the ognES.py process is still running
    if len(data) < 40:
        continue                            # nothing else to do

    ix = data.find('>')
    cc = data[0:ix]
    cc = cc.upper()
    data = cc+data[ix:]
    msg = {}

    msg = parseraprs(data, msg)             # parser the data
    if msg == -1:			    # parser error
            print("Parser error:", data)
            continue
    ident = msg['id']          	            # id
                                            # get the information once parsed
    ptype       = msg['aprstype']
    longitude   = msg['longitude']
    latitude    = msg['latitude']
    altitude    = msg['altitude']
    path        = msg['path']
    if path not in paths:
       paths.append(path)
    if path == 'aprs_aircraft' or path == 'flarm' or path == 'tracker':
        if 'speed' in msg :
            speed   = msg['speed']
        if 'course' in msg :
            course  = msg['course']
    source      = msg['source']
    if len(source) > 4:
        source = source[0:3]
    otime       = msg['otime']

    if longitude == -1 or latitude == -1:
        continue
    callsign = ident                        # get the call sign FLARM ID

    if (data.find('TCPIP*') != -1) or path == 'aprs_receiver':         # ignore the APRS lines
        ident = callsign                    # station ID
        if not ident in fsloc:
                                            # save the loction of the station
            fsloc[ident] = (latitude, longitude)
            fsmax[ident] = 0.0              # initial coverage zero
            fsfix[ident] = 0                # initial coverage zero
            #print "ID:", ident, data[0:10], latitude, longitude
        if ident == None:
            ident = data[0:data.find('>')]
            print("ID:", ident, data[0:10])
                                            # save the loction of the station
            fsloc[ident] = (latitude, longitude)
            fsmax[ident] = 0.0              # initial coverage zero
            fsfix[ident] = 0                # initial coverage zero
        continue                            # go for the next record
    if cc in blacklist:
        continue
    idname = data[0:9]                      # exclude the FLR part
    if idname[0:3] == 'RND':
        continue
    station = msg['station']                # get the station ID
    if ptype == 'status':		    # if OGN status report
        continue
    if not source in fsour:		    # did we see this source
        fsour[source] = 1		    # init the counter
    else:
        fsour[source] += 1		    # increase the counter
    if station == "FLYMASTER":
        continue
    # or frenchsta(station):  # only Chilean or Spanish or frenchstations
    if ((hostname == "CHILEOGN" or hostname == "OGNCHILE") and source == "OGN") or source == "SPOT" or spanishsta(station):
        if not ident in fid:                # if we did not see the FLARM ID
            fid[ident] = 0                  # init the counter
            fsta[ident] = station           # init the station receiver
                                            # take off time/ initial seeing  - null for the time being
            ftkot[ident] = 0
                                            # landing  time - null for the time being
            flndt[ident] = 0
            cout += 1                       # one more file to create
                                            # prepare the IGC header
            if ident[3:9] in kglid.kglid:   # if it is a known glider ???
                fd = open(datapath+tmp+'FD'+dte+'.'+station+'.' +
                          kglid.kglid[ident[3:9]].strip()+'.'+idname+'.IGC', 'w')
            else:
                fd = open(datapath+tmp+'FD'+dte+'.' +
                          station+'.'+idname+'.IGC', 'w')

            fd.write('AGNE001GLIDER\n')     # write the IGC header
            fd.write('HFDTE'+dte+'\n')      # write the date on the header
            if ident[3:9] in kglid.kglid:
                                            # write the registration ID
                fd.write('HFGIDGLIDERID: '+kglid.kglid[ident[3:9]]+'\n')
            else:
                                            # if we do not know it write the FLARM ID
                fd.write('HFGIDGLIDERID: '+ident+'\n')
            ffd[ident] = fd                 # save the file descriptor
                                            # increase the number of records read
        fid[ident] += 1
                                            # scan for the body of the APRS message
        p1 = data.find(':/')+2
        if data[p1+6] == 'z':		    # if date is Z with date
            hora = data[p1+2:p1+6]+'00'     # get HHMM
        else:
            hora = data[p1:p1+6]            # get the GPS time in UTC

        lati = data[p1+7:p1+11]+data[p1+12:p1+14] + \
            '0'+data[p1+14]                 # get the latitude
        longi = data[p1+16:p1+21]+data[p1+22:p1+24] + \
            '0'+data[p1+24]                 # get the longitude
        altim = altitude                    # convert the altitude in metersa

        if altim == None or (altim > 15000 or altim < 0):
            altim = 0
        alti = '%05d' % altim               # convert it to an string

        ffd[ident].write('B'+hora+lati+longi+'A00000'+alti + '\n')  # format the IGC B record
                                            # include the original APRS record for documentation
        ffd[ident].write('LGNE '+data)

                                            # if we do not have the take off time ??
        if speed > 50 and ftkot[ident] == 0:
            ftkot[ident] = otime            # store the take off time
            ftkok[otime] = ident            # list by take off time
                                            # if we do not have the take off time ??
        if speed < 20 and speed > 5 and ftkot[ident] != 0:
            flndt[ident] = otime            # store the landing time
        if station in fsloc:                # if we have the station yet
                                            # increase the number of fixes for that station
            fsfix[station] += 1
                                            # distance to the station
            distance = vincenty((latitude, longitude), fsloc[station]).km
            if distance > 300.0:
                print(">>>Distcheck: ", distance, data, cin)
            elif distance > fsmax[station]: # if higher distance
                fsmax[station] = distance   # save the new distance
        if altim > tmaxa:
            tmaxa = altim                   # maximum altitude for the day
            tmaxt = hora                    # and time
            tmid = ident                    # who did it
            tmsta = station                 # station capturing the max altitude
            mlong = longitude               # longitude of the max alt point
            mlati = latitude                # latitude
        cin += 1                            # one more record read


# -----------------  final process ----------------------
datafilei.close()                           # close the input file
datef = datetime.now()                      # get the time & date
if tmid != 0 and tmid[3:9] in kglid.kglid:  # if it is a known glider ???
    gid = kglid.kglid[tmid[3:9]]            # report the registration
else:
    gid = tmid                              # just report the flarmid
# geolocator = Nominatim(timeout=5)         # define the geolocator, we need 5 second timeout
# loc = geolocator.reverse([mlati,mlong])   # locate the point of maximun altitue for the day.

# addr=loc.address                          # the location name
# addr=addr.encode('utf8')                  # convert it to UTF-8
# addr=str(addr)                            # convert to str just in case, in order to avoid problems when is redirected to a file.
addr = ' '
print("Sources:", fsour)
if prt:
    print("Maximun altitude for the day  :", tmaxa, ' meters MSL at:', tmaxt, 'Z by:', gid, 'Station:', tmsta, "At: ", mlati, mlong, addr)
if prt:
    print("Total number of fixes today   :", tfixs)
if prt:
    print('Bye ... Time now and Time used:', datef, datef - \
        date)                               # report the processing time
