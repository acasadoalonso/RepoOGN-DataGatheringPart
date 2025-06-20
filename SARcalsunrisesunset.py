#!/usr/bin/python3
import sys
import socket
sys.path.insert(0, '/nfs/OGN/src/funcs')
from parserfuncs import SRSSgetjsondata, getinfoairport
pgmver="1.1"
print("\n\nStart calSunriseSunset ", pgmver)
print("===========================")
import config
hostname = socket.gethostname()
import platform
print("Python version:", platform.python_version())
import git
try:
   repo = git.Repo(__file__, search_parent_directories=True)
   sha = repo.head.object.hexsha
except:
   sha="no sha"
print ("Git commit:", sha, "\n\n")

#
#	get the sunrise/sunset data
#

if getinfoairport (config.location_name) != None:
   print(getinfoairport (config.location_name))
   location_latitude =  str(getinfoairport (config.location_name)['lat'])
   location_longitude = str(getinfoairport (config.location_name)['lon'])
   
else:
   
   location_latitude=config.location_latitude
   location_longitude=config.location_longitude
print("Location coordinates:", location_latitude, location_longitude, "at: ", config.location_name)
print("===================================")
lat=location_latitude
lon=location_longitude

timeepoc=SRSSgetjsondata(str(lat), str(lon), prt=False)
print (timeepoc, " ", hostname, config.DBpath+config.APP+".sunset" )
sunsetfile = open (config.DBpath+config.APP+".sunset", 'w') # create a file just to mark that we are alive
sunsetfile.write(str(timeepoc)+"\n") # write the time as control
sunsetfile.close()               # close the alive file

print("===================================\n\n")
