#!/usr/bin/python
#
# This program reads the the records received from the OGN APRS server for SPAIN
# and generates IGC files for each flight
# It runs 30 minutes after the sunset in Lillo(TO) - LELT
#
# Author: Angel Casado - May 2015
#
import datetime 
import time
import sys
import os
import kglid                                # import the list on known gliders
from   libfap import *
from   parserfuncs import *

def spanishsta(station):                    # return true if is an spanish station
    if station[0:2] == 'LE' or station [0:5] == 'CREAL':
        return True
    else:
        return False
#
# ---------- main code ---------------
#

print "Start process OGN records V1.4"
print "=============================="
dtereq =  sys.argv[1:]
if dtereq and prtreq[0] == 'date':
    dter = True                             # request the date
else:
    dter = False                            # do not request the date
cin  = 0                                    # input record counter
cout = 0                                    # output file counter
date=datetime.datetime.now()                         # get the date
dte=date.strftime("%d%m%y")                 # today's date
fname='DATA'+dte+'.log'                     # file name from logging

#fname='DATA170515.log'                     # example of file name 

if not dter:                                # check if we need to request date
    print 'User: ', os.environ['USER']      # tell that
    fname='DATA'+dte+'.log'                 # build the file name with today's date
else:
    dte=raw_input('Enter date:')            # otherwise ask for the date
    if dte == '':                           # if no input 
        dte=date.strftime("%d%m%y")         # use the default
    fname='DATA'+dte+'.log'                 # build the file name with the date entered
    
print 'File name: ', fname, 'Process date/time:', date.strftime(" %d-%m-%y %H:%M:%S")     # display file name and time

datafilei = open(fname, 'r')                # open the file with the logged data
fid=  {'NONE  ' : 0}                        # FLARM ID list
fsta= {'NONE  ' : 'NONE  '}                 # STATION ID list
ffd=  {'NONE  ' : datafilei}                # file descriptor list
ftkot={'NONE  ' : 0}                        # take off time
flndt={'NONE  ' : 0}                        # take off time
 
print "libfap_init"
libfap.fap_init()

while True:                                 # until end of file 
    data=datafilei.readline()               # read one line
    if not data:                            # end of file ???
        print 'Input records: ',cin, 'Ouput files:',cout # report number of records read and files generated
        k=list(fid.keys())                  # list the IDs for debugging purposes
        k.sort()                            # sort the list
        
        for key in k:                       # report data
            if key in kglid.kglid:          # if it is a known glider ???
                r=kglid.kglid[key]          # get the registration
            else:
                r='NOREG '                  # no registration
            print key, '=>', 'Base:', fsta[key], 'Reg:', r, 'Take off:', ftkot[key], 'Landing:', flndt[key],'Nrecs:', fid[key]
                                            # report FLARM ID, station used,  record counter, registration, take off time and landing time
            ffd[key].close()                # and close all the files
        break                               # work done

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
    
    if (data.find('TCPIP*') != -1):         # ignore the APRS lines
        continue                            # go for the next record
    id=data[3:9]                            # exclude the FLR part
    station=data[19:23]                     # get the station identifier
    if spanishsta(station):                 # only Spanish stations
        if not id in fid :                  # if we did not see the FLARM ID
            fid  [id]=0                     # init the counter
            fsta [id]=station               # init the station receiver
            ftkot[id]=0                     # take off time/ initial seeing  - null for the time being
            flndt[id]=0                     # landing  time - null for the time being
            cout += 1                       # one more file to create
                                            # prepare the IGC header
            if id in kglid.kglid:           # if it is a known glider ???
                fd = open('FD'+dte+'.'+station+'.'+kglid.kglid[id]+'.'+id+'.IGC', 'w')
            else:
                fd = open('FD'+dte+'.'+station+'.'+id+'.IGC', 'w')
            fd.write('AGNE001GLIDER\n')     # write the IGC header
            fd.write('HFDTE'+dte+'\n')      # write the date on the header
            if id in kglid.kglid:
                fd.write('HFGIDGLIDERID: '+kglid.kglid[id]+'\n')    # write the registration ID
            else:
                fd.write('HFGIDGLIDERID: '+id+'\n')                 # if we do not know it write the FLARM ID
            ffd[id] = fd                    # save the file descriptor
        fid[id] +=1                         # increase the number of records read
        p1=data.find(':/')+2                # scan for the body of the APRS message
        hora=data[p1:p1+6]                  # get the GPS time in UTC
        long=data[p1+7:p1+11]+data[p1+12:p1+14]+'0'+data[p1+14]         # get the longitude
        lati=data[p1+16:p1+21]+data[p1+22:p1+24]+'0'+data[p1+24]        # get the latitude
        p2=data.find('/A=')+3               # scan for the altitude on the body of the message
        altif=data[p2+1:p2+6]               # get the altitude in feet
        altim=int(altif)/3.280575           # convert the altitude in meters
        alti='%05d' % altim                 # convert it to an string
        ffd[id].write('B'+hora+long+lati+'A00000'+alti+'\n') # format the IGC B record
        ffd[id].write('LGNE '+data)         # include the original APRS record for documentation
 
        if speed > 50 and ftkot[id] == 0:   # if we do not have the take off time ??
                ftkot[id] = otime           # store the take off time
        if speed < 20 and speed > 5 and ftkot[id] != 0:   # if we do not have the take off time ??
                flndt[id] = otime           # store the landing time
        cin +=1                             # one more record read
        
datafilei.close()                           # close the input file
datef=datetime.datetime.now()               # get the time & date
                                            # Close libfap.py to avoid memory leak
libfap.fap_cleanup()
print 'Bye ... Time and Time used:', datef, datef-date      # report the processing time

    
