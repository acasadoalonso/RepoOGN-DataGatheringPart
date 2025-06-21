#!/usr/bin/python3
import sys
import time
import socket
import os
sys.path.insert(0, '/nfs/OGN/src/funcs')
pgmver="1.1"
print("\n\nStart calSunriseSunset ", pgmver)
print("===========================")
from parserfuncs import SRSSgetjsondata, getinfoairport
hostname = socket.gethostname()
import platform
print("Python version:", platform.python_version())
import git
try:
   repo = git.Repo(__file__, search_parent_directories=True)
   sha = repo.head.object.hexsha
except:
   sha="no sha"
print("Program Version:", time.ctime(os.path.getmtime(__file__)))
print ("Git commit:", sha, "\n\n")
import config

#
#	get the sunrise/sunset data
#

if getinfoairport (config.location_name) != None:
   print("From getinfoairport:\n", getinfoairport (config.location_name))
   location_latitude =  str(getinfoairport (config.location_name)['lat'])
   location_longitude = str(getinfoairport (config.location_name)['lon'])
   
else:
   print("From config file:\n")  
   location_latitude=config.location_latitude
   location_longitude=config.location_longitude
print("\nLocation coordinates:", location_latitude, location_longitude, "at: ", config.location_name)
print("===================================")
lat=location_latitude
lon=location_longitude

timeepoc=SRSSgetjsondata(str(lat), str(lon), prt=False)
print (timeepoc, " ", hostname, config.DBpath+config.APP+".sunset" )
sunsetfile = open (config.DBpath+config.APP+".sunset", 'w') # create a file just to mark that we are alive
sunsetfile.write(str(timeepoc)+"\n") # write the time as control
sunsetfile.close()               # close the alive file

print("===================================\n\n")
