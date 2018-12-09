#!/usr/bin/python
import cgi
import os
import sys
import cgitb
import urllib2

from xml.etree.ElementTree import parse, fromstring
import sys
import datetime
streq =  sys.argv[1:]
if streq :
    sta = streq[0]                             # request the date
else:
    sta = "LEMD"                            # do not request the date

#html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station are: </H1> <HR> <P> %s </P> </HR> """
html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station (%s) are: </H1> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center>========</html>"""

www=True

if www: print (html1 % sta)
if www: print html2
################

if www: print "<a> <H1>TAFOR </H1></a>"
url =('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=25' % sta)
f = urllib2.urlopen(url)
root = parse(f)

fc = list(root.iterfind('data/TAF'))
print "<a> ", fc," </a>"
for taf in fc:
    rawtext=taf.findtext('raw_text')
    print '<a>', rawtext, '</a>' 
f.close()
if www: print html3
################
