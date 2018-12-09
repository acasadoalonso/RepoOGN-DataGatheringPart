#!/usr/bin/python
import cgi
import os
import cgitb
import sqlite3
import sys
import config
from   geopy.geocoders import Nominatim
def scandir (dir, rpath, html4, curs, curs2):
	nlines=0
	ld = os.listdir(dir)	
	ld.sort()
	for f in ld:
		if f[0:2] == "FD" and f.find(rg) != -1:
			id =f[-13:-4]
			dte=f[2:8]
			alt=0.0
			dst=0.0
			cnt=0
			addr=''
                    	selcmd="select count(*), max(altitude) as maxa, max(distance) as maxd from OGNDATA where idflarm = '%s' and date = '%s' "% (id, dte)
                    	curs.execute(selcmd)
			reg=curs.fetchone()
			if reg and reg != None:
				cnt=reg[0]
				if cnt > 0:
					alt=reg[1]
					dst=reg[2]
				#geolocator = Nominatim(timeout=5)
                    		execmd="select max(altitude) as maxa, latitude, longitude from OGNDATA where idflarm = '%s' and date = '%s' "% (id, dte)
                    		curs2.execute(execmd)
				reg=curs2.fetchone()
				if reg and reg != None:
					malt=reg[0]
					if malt == alt:
						lati=reg[1]
						long=reg[2]
						addr=''
						#loc = geolocator.reverse([lati,long])
						#if loc.address != None:
							#addr=(loc.address).encode('utf8')
						addr=' '
					else:
						lati=0.0
						long=0.0
						addr=''
			nlines += 1
			if cnt > 0:
				details =  (" ==> Count(%4d) MDist(%5.1f) MAlt(%6.1f) Lat(%7.4f) Long(%7.4f) %s " % (cnt, dst, alt, lati, long, addr))
			else:
				details = " "
			fn=html4 + rpath + '/' + f.lstrip()
			fname=("FN:%-33s" % f)
			print fn , '">MAP</a>', "<a>", fname, details,  "</a>"
		elif (os.path.isdir(dir+'/'+f)):
			nlines +=scandir(dir+'/'+f, rpath+'/'+f, html4, curs, curs2)
	return(nlines)
#
# Get IGC file by registration
#

rootdir = config.DBpath+"/fd"
if config.MySQL:
        import MySQLdb                  # the SQL data base routines^M
        conn=MySQLdb.connect(host=config.DBhost, user=config.DBuser, passwd=config.DBpasswd, db=config.DBname)
else:
        import sqlite3
        conn=sqlite3.connect(config.DBpath+config.SQLite3)

curs=conn.cursor()
curs2=conn.cursor()

cgitb.enable()
# select distinct date  from OGNDATA where idflarm=(select idglider from GLIDERS where registration = 'D-2520') ;
regist =  sys.argv[1:]			# first parameter
if regist :
    rr = regist[0]                      # get the registration
else:
    rr = ''                        
html1="""<head><meta charset="UTF-8"></head><TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The flights for the selected registration are: </H1> <HR> <P> %s </P> </HR> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center>"""
html4='<a href="http://cunimb.net/igc2map.php?lien=http://'+config.reposerver+'/DIRdata/fd'
nlines=0

if rr == '':
	print (html1 % 'Invalid  registration')
else:
	rg=rr.strip()
	rg=rg.upper()
       	cmd="select cn from GLIDERS where registration = '%s' " % rg
       	curs.execute(cmd)
	reg=curs.fetchone()
	if reg and reg != None:
		cn=reg[0]
	else:
		cn=''
	vd = ('Valid registration: %-s %s:' % (rg,cn))
	print (html1 % vd)
	print html2
	nlines=scandir(rootdir, "", html4, curs, curs2)
	if nlines == 0:
		print "No flights found for:", rg 
	print html3
	

