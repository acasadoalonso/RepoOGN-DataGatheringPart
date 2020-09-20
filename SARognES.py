#!/usr/bin/python3
#
# Python code to show access to OGN Beacons
#
# Version for gathering all the records from OGN APRS

from ctypes import *
import socket
import time
import string
import ephem
import pytz
import sys
import signal
import atexit
import os
import socket
import ksta                             # import the list on known gliders
from ognddbfuncs import *               # import the OGN DDB functions
from datetime import datetime
sys.path.insert(0, '/nfs/OGN/src/funcs')
from parserfuncs import *               # the ogn/ham parser functions
from time import sleep                  # the sleep


def shutdown(sock, datafile, tmaxa, tmaxt, tmid):
                                        # shutdown before exit
    sock.shutdown(0)                    # shutdown the connection
    sock.close()                        # close the connection file
    datafile.close()                    # close the data file
    if (os.stat(OGN_DATA).st_size == 0):
        os.system("rm "+OGN_DATA)
    # report number of records read and IDs discovered
    print('Records read:', cin, ' Ids found: ', cout)
    k = list(fid.keys())                # list the IDs for debugging purposes
    k.sort()                            # sort the list
    for key in k:                       # report data
        gid = 'Noreg '                  # for unknown gliders
        if spanishsta(key) or frenchsta(key):
            if key in ksta.ksta:
                gid = ksta.ksta[key]   # report the station name
            else:
                gid = "NOSTA"           # marked as no sta
        else:
            # if it is a known glider ???
            if key != None and getognchk(key[3:9]):
                gid = getognreg(key[3:9])   # report the registration

        if fmaxs[key] > 0:
            # report FLARM ID, station used, registration and record counter
            print(key, '=>', fsta[key], gid, fid[key], "Max alt:", fmaxa[key], "Max speed:", fmaxs[key])
        else:
            print(key, '=>', fsta[key], gid, fid[key], "Max alt:", fmaxa[key])

            # report now the maximun altitude for the day
    if getognchk(tmid[3:9]):            # if it is a known glider ???
        gid = getognreg(tmid[3:9])      # report the registration
    else:
        gid = tmid                      # use the ID instead
    print("Maximun altitude for the day:", tmaxa, ' meters MSL at:', tmaxt, 'by:', gid, 'Station:', tmsta)
    print("Number of RELAY packets:", relaycnt, relaycntr)
    if relaycnt > 0:
        print("Relays:", relayglider)
    print("Stations:", stations)
    print("Sources:", sources)
    print("Aircraft types:", acfttype)
    print (paths)
    local_time = datetime.now()
    print("Time now:", local_time, "Local time.")
    try:
        os.remove(config.APP+".alive")
    except:
        print("No OGN.live")
    return

#########################################################################


def signal_term_handler(signal, frame):	# signal handler for SIGTERM
    print('got SIGTERM ... shutdown orderly Time: ', datetime.now())
    shutdown(sock, datafile, tmaxa, tmaxt, tmid)  # shutdown orderly
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_term_handler)

#----------------------ogn_main.py start-----------------------
pgmver = "V2.2"
fid = {'NONE  ': 0}                     # FLARM ID list
fsta = {'NONE  ': 'NONE  '}             # STATION ID list
fmaxa = {'NONE  ': 0}                   # maximun altitude
fmaxs = {'NONE  ': 0}                   # maximun speed
stations = []				# stations
sources  = []				# sources found
acfttype = []				# aircraft types found
CCerrors = []				# station with parser errors
cin = 0                                 # input record counter
cout = 0                                # output file counter
loopcnt = 0                             # loop counter
err = 0				        # init the error counter
relaycnt = 0				# counter of relay packets
relaycntr = 0				# counter of relay packets
relayglider = {}			# list of relaying gliders
maxerr = 50				# max number of input error before gaive up
tmaxa = 0                               # maximun altitude for the day
tmaxt = 0                               # time at max altitude
tmid = 'None     '                      # glider ID obtaining max altitude
tmsta = '         '                     # station capturing max altitude
hostname = socket.gethostname()
if hostname == 'CHILEOGN' or hostname == "OGNCHILE":
    print("Start ognCL CHILE ", pgmver)
else:
    print("Start ognES SPAIN ", pgmver)
print("========================")

import config
prtreq = sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False

if os.path.exists(config.PIDfile):
    raise RuntimeError("SAR already running !!!")
    exit(-1)
#
APP = "SAR"                             # the application name

with open(config.PIDfile, "w") as f:
    f.write(str(os.getpid()))
    f.close()
atexit.register(lambda: os.remove(config.PIDfile))

# create socket & connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
# sock.connect(('aprs.glidernet.org',14580))
sock.connect((config.APRS_SERVER_HOST, config.APRS_SERVER_PORT))
print("Socket sock connected")

# logon to OGN APRS network

login = 'user %s pass %s vers Py-REPO %s %s' % (config.APRS_USER, config.APRS_PASSCODE, pgmver, config.APRS_FILTER_DETAILS)
sock.send(login.encode('UTF-8'))

# Make the connection to the server
sock_file = sock.makefile(mode='rw')    # make read/write as we need to send the keep_alive


print("APRS Version:", sock_file.readline())
sleep(2)
print("APRS Login request:", login)
print("APRS Login reply:  ", sock_file.readline())


start_time = time.time()
local_time = datetime.now()
fl_date_time = local_time.strftime("%y%m%d")
OGN_DATA = "DATA" + fl_date_time+'.log'
print("OGN data file is: ", OGN_DATA)
datafile = open(OGN_DATA, 'a')
alive(config.APP, first="yes")					# mar that we are alive
keepalive_count = 1
keepalive_time = time.time()

#
#-----------------------------------------------------------------
# Initialise API for computing sunrise and sunset
#-----------------------------------------------------------------
#
location = ephem.Observer()
location.pressure = 0
location.horizon = '-0:34'  # Adjustments for angle to horizon

location.lat, location.lon = config.FLOGGER_LATITUDE, config.FLOGGER_LONGITUDE
date = datetime.now()
next_sunrise = location.next_rising(ephem.Sun(), date)
next_sunset = location.next_setting(ephem.Sun(), date)
print("Sunrise today is at: ", next_sunrise, " UTC ")
print("Sunset  today is at: ", next_sunset,  " UTC ")
print("Time now is: ", date, "Local time, Process ID:", os.getpid(), " on Hostname:", hostname)
nerrors = 0
paths=[]
try:

    while True:
        # Loop for a long time with a count, illustrative only
        current_time = time.time()
        elapsed_time = current_time - keepalive_time
        if (current_time - keepalive_time) > 180:        # keepalives every 3 mins
            try:
                # write something to the APRS server to stay alive !!!
                rtn = sock_file.write("#Python ognES App\n\n")
                sock_file.flush() 		# Make sure keepalive gets sent. If not flushed then buffered
                datafile.flush()		# use this opportunity to flush the data file
                alive(config.APP)		# and mark that we are still alive
                run_time = time.time() - start_time
                if prt:
                    print("Send keepalive no: ", keepalive_count, " After elapsed_time: ", int(
                        (current_time - keepalive_time)), " After runtime: ", int(run_time), " secs")
                keepalive_time = current_time
                keepalive_count = keepalive_count + 1
            except Exception as e:
                print((
                    'Something\'s wrong with socket write. Exception type is %s' % (repr(e))))
                print("Time now:", current_time, datetime.now())
                nerrors = nerrors + 1           # increase the counter of errors
                if (nerrors > 30):              # if number of errors is bigger than 30
                    sock_file.close()           # try to close the file
                    sock_file = sock.makefile(mode='rw')    # re make read/write as we need to send the keep_alive
                    nerrors = 0

        location.date = ephem.Date(datetime.utcnow())
        date = datetime.utcnow()
        s = ephem.Sun()
        s.compute(location)
        # Defn of Twilight is: Sun is 6, 12, 18 degrees below horizon (civil, nautical, astronomical)
        twilight = -6 * ephem.degree
        if s.alt < twilight:
            print("At Sunset now ... Time is:", date, "UTC ...  Next sunset is: ", next_sunset,  " UTC")
            shutdown(sock, datafile, tmaxa, tmaxt, tmid)
            print("At Sunset ... Exit")
            exit(0)

        if prt:
            print("In main loop. Count= ", loopcnt)
            loopcnt += 1
        try:
            # Read packet string from socket
            packet_str = sock_file.readline()
            if len(packet_str) > 0 and packet_str[0] != "#":
                datafile.write(packet_str)

        except socket.error:
            print("Socket error on readline")
            continue
        # A zero length line should not be return if keepalives are being sent
        # A zero length line will only be returned after ~30m if keepalives are not sent
        if len(packet_str) == 0:
            err += 1
            if err > maxerr:
                print("Read returns zero length string. Failure.  Orderly closeout")
                date = datetime.now()
                print("UTC now is: ", date)
                break
            else:
                sleep(5)		    # sleep 5 seconds
                continue
        if packet_str[0] == "#":            # the time alive from server 
            continue
#   ready to handle a record

        ix = packet_str.find('>')           # find the station
        cc = packet_str[0:ix]               # extract the station
        cc = cc.upper()                     # convert it to upper case
                                            # change the packet to be in uppercase
        packet_str = cc+packet_str[ix:]
        msg = {}
        data=packet_str                     # the input data ....
        # Parse packet using ogn_client into fields to process
        msg = parseraprs(data, msg)         # parser the data
        if msg == -1:			    # parser error
            if cc not in CCerrors:
               print("Parser error:", data)
               CCerrors.append(cc)
            continue

        if len(packet_str) > 0 and packet_str[0] != "#":
            ptype       = msg['aprstype']
            longitude   = msg['longitude']
            latitude    = msg['latitude']
            altitude    = msg['altitude']
            if altitude == None:
                altitude = 0
            path        = msg['path']
            if path not in paths:
                paths.append(path)
            ident       = msg['id']
            speed=0.0
            course=0
            if path == 'aprs_aircraft' or path == 'flarm' or path == 'tracker':
                if 'speed' in msg :
                    speed   = msg['speed']
                if 'course' in msg :
                    course  = msg['course']
            dst_callsign = msg['id']
            source      = msg['source']
            if len(source) > 4:
                source = source[0:3]
            otime       = msg['otime']

            station = msg['station']
            if 'relay' in msg:
                relay = msg['relay']
            else:
                relay = ''
            # if std records
            if 'acfttype' in msg:
               acftt=msg['acfttype']
               if not acftt in acfttype:
                  acfttype.append(acftt)
                  
            if path == 'aprs_aircraft' or path == 'flarm' or path == 'tracker':
                if not station in stations:
                    # add it to the list of stations ...
                    stations.append(station)
                    #print "SSS", station
                if not source in sources:
                    # add it to the list of sources ...
                    sources.append(source)
                if relay == "RELAY" or relay == "OGNDELAY":
                    relaycntr += 1
                if relay[0:3] == "OGN":
                    relaycnt += 1
                    if prt:
                        print("RELAY:", path, station, id, destination, header, otime)
                    if not ident in relayglider:
                        relayglider[ident] = relay[0:9]

            elif path == 'aprs_receiver' or relay == 'TCPIP' or path == "NOPATH":
                data = packet_str
                ssep = data.find('>')               # find the separatora
                if ssep != -1:
                    station = data[0:ssep]          # get the station identifier
                    station = station.upper()       # translate to uppercase
                    ident = station
                else:
                    ident = "NOREG"

            else:
                station = ident                     # just the station itself
            if prt:                                 # just for debugging
                print('Packet returned is: ', packet_str)
                print('Message: ', msg)
                print('OTime:', otime, "Source:", source, "\n-------------------------------------------------------\n")
            if not ident in fid:                    # if we did not see the FLARM ID yet
                fid[ident] = 0                      # init the counter
                fsta[ident] = station               # init the station receiver
                fmaxa[ident] = altitude             # maximun altitude
                fmaxs[ident] = speed                # maximun speed
                cout += 1                           # one more file to create

            cin += 1                                # increase total input records
                                                    # increase the number of records read
            fid[ident] += 1
            if altitude >= fmaxa[ident]:            # check for max altitude of the day
                fmaxa[ident] = altitude
                if altitude > tmaxa and (not spanishsta(ident) and not frenchsta(ident)):
                    tmaxa = altitude                # maximum altitude for the day
                    tmaxt = date                    # date and time
                    tmid = ident                    # who did it
                    tmsta = station                 # station capturing the max altitude
            if speed >= fmaxs[ident]:               # check for max speed of the day
                fmaxs[ident] = speed


except KeyboardInterrupt:
    print("Keyboard input received, shutdown ...")
    shutdown(sock, datafile, tmaxa, tmaxt, tmid)  # shutdown orderly
    exit(1)
#
except TypeError as e:
    print("TypeError: ...",e)
    ## print the record for debugging purposes
    print(">>>>>>>> Packet: ", packet_str)
    shutdown(sock, datafile, tmaxa, tmaxt, tmid)  # shutdown orderly
    exit(1)


# report number of records read and files generated
print('Counters:', cin, cout)
if (os.stat(OGN_DATA).st_size == 0):
    os.system("rm "+OGN_DATA)
shutdown(sock, datafile, tmaxa, tmaxt, tmid)
print("Exit now ...", err)
exit(1)
