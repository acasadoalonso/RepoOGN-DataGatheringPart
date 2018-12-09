#!/usr/bin/python
import cgi
import os
import sys
import cgitb
import sqlite3
import time
import datetime
import config

cgitb.enable()
#
# This script generates all the IGC files that are live now and present the list to the user
#

execfilename="/nfs/OGN/src/processogn.py"
tempdir     ="/nfs/OGN/DIRdata/tmp/"
datapath    ="/nfs/OGN/DIRdata/"


html1="""<TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>Today's flights for the selected registration are: </H1> <HR> <P> %s </P> </HR> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center>"""
html4='<a href="http://cunimb.net/igc2map.php?lien=http://'+config.reposerver+'/DIRdata/tmp/%s'

nlines=0                                            # init the number of lines(files) shown
# select distinct date  from OGNDATA where idflarm=(select idglider from GLIDERS where registration = 'D-2520') ;
regist =  sys.argv[1:]                  # first parameter
if not regist :
    	rr = ''
	print (html1 % 'Invalid  registration')
else:
    	rr = regist[0]                      # get the registration
	rg=rr.strip()                               # clean the whitespace
	rg=rg.upper()                               # translate to upper case
	
	date=datetime.datetime.now()                # get the date
	dte=date.strftime("%y%m%d")                 # today's date
	fname='DATA'+dte+'.log'                     # file name from logging
	if not	os.path.exists(datapath+fname):	    # test of this file exists, if so is because ognES.py is running
		print "No active flights at this time ...", fname
		quit()				    # nothing else to do
	cmd="rm "+tempdir+"FD* "		    # remove all the previous FD files
	os.system(cmd)
	execfile(execfilename)                      # invoke to processogn.py in order to generate the IGC file of today
	print “TTT”
	vd = ('Valid registration: %-s:' % rg)      # prepate the literal to show
	print (html1 % vd)                          # tell that         
	print html2                                 # prepare the table header
	if rg == "ALL":                             # if all the files, just ignore 
		rg="FD"
	
	ld=os.listdir(tempdir)	 	            # scan the tmp directory generate by processogn.py	
	ld.sort()
	for f in ld:				    # go thru the list
		if f[0:2] == "FD" and f.find(rg) != -1: # only the FD* files (IGC)
			fn=(html4 % f.lstrip())     # prepare the line to show --- we include here the hyperlink to cunimb.net
			id =f[-10:-4]               # get the ID (not used)               
			dte=f[2:8]
			nlines += 1
			fname=("FN:%-33s" % f)      # prepare the filename
			statinfo = os.stat(tempdir+f)
			print fn , '">MAP</a>', "<a>", fname, ("Size(%06d)"% statinfo.st_size), " </a>"    # put the line for that file with the links to cunim.net
	if nlines == 0:				    # check if flights found
		if rg == "FD":
			rg="ALL"
		print "No flights found for:", rg 
	print html3                                 # place the end of the table
quit()                                              # all done
	

