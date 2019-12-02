#!/usr/bin/python3
import sys
import socket
sys.path.insert(0, '/nfs/OGN/src/funcs')
from parserfuncs import *
import config
hostname = socket.gethostname()

#
#	get the sunrise/sunset data
#

lat=config.location_latitude
lon=config.location_longitude
timeepoc=SRSSgetjsondata(lat, lon, prt=True)
print (timeepoc, " ", hostname, config.DBpath+config.APP+".sunset" )
sunsetfile = open (config.DBpath+config.APP+".sunset", 'w') # create a file just to mark that we are alive
sunsetfile.write(str(timeepoc)+"\n") # write the time as control
sunsetfile.close()               # close the alive file
