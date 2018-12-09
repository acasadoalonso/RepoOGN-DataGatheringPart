#!/usr/bin/python 
import json
import cgi
import cgitb
import os
import urllib2
import sqlite3
import os
cgitb.enable()

dbpath ="/nfs/OGN/DIRdata/"
html1="""<TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>Statistics of the OGN receiver stations:: </H1> <HR> <P> %s </P> </HR> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center>"""
filename=dbpath+'OGN.db'                                    # open th DB in read only mode
fd = os.open(filename, os.O_RDONLY)
conn = sqlite3.connect('/dev/fd/%d' % fd)
cursD=conn.cursor()  
form=cgi.FieldStorage()
print("Content-type: text/html\n") 
rr=form['regis'].value                      # get the registration ID or ALL
rg=rr.strip()                               # clean the whitespace
rg=rg.upper()                               # translate to upper case
vd = ('Valid registration: %-s:' % rg)      # prepate the literal to show
print (html1 % vd)                          # tell that
print html2                                 # cursor for the ogndata table
print "<a> Month   Positions   Gliders </a>"
if rg == "ALL":
	cursD.execute('select idrec, descri from RECEIVERS ')             # get all the receivers
else:
	cursD.execute('select idrec, descri from RECEIVERS where idrec = ? ', [rg])             # get all the receivers

for row in cursD.fetchall():                                    # search all the rows
	id=row[0]
	desc=row[1]
	if (id == None or id == "NONE"):
		continue
	j = urllib2.urlopen('http://flarmrange.onglide.com/api/1/stats?station='+id+'&grouping=month')
	j_obj = json.load(j)
	j=json.dumps(j_obj, indent=4)
	stats=j_obj["stats"]
	
	print "<a>",id, ":", desc, "</a>"
	for month  in stats:
        	#print month
#
        	time= month["t"]
        	pos= month["p"]
        	gliders= month["g"]
        	rows= month["n"]
        	temp= month["temp"]
		if pos != 0:
			print "<a>", time, "%9.0f"%pos,  "%9.0f"%gliders, "</a>"
print html3
cursD.close()
os.close(fd)
