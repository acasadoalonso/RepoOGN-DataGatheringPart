
#-------------------------------------
# OGN-Silent Wings interface --- Settings 
#-------------------------------------
#
#-------------------------------------
# Setting values
#-------------------------------------
#
import socket
APRS_SERVER_HOST = socket.gethostname()
APRS_SERVER_PORT = 14580
APRS_USER = 'APRSLOG'
# APRS_PASSCODE = -1   #Read only

APRS_PASSCODE = 27566  							# See http://www.george-smart.co.uk/wiki/APRS_Callpass
APRS_FILTER_DETAILS_1 = "filter r/+42.12/+0.48/6000 r/-33.12/-70.48/800 \n " 			# two areas
APRS_FILTER_DETAILS_2 = "filter r/-33.12/-70.48/800 \n " 		# one areas
AFD={"CASADOUBUNTU": APRS_FILTER_DETAILS_1, \
     "SWCHILE":      APRS_FILTER_DETAILS_1, \
    }
APRS_FILTER_DETAILS = AFD[socket.gethostname()]
									# Check that APRS_USER and APRS_PASSCODE are set
assert len(APRS_USER) > 3 and len(str(APRS_PASSCODE)) > 0, 'Please set APRS_USER and APRS_PASSCODE in settings.py.'
									# aprs.glidernet.org on port 14580.

DBpath=r"/nfs/OGN/SWdata/"						# data directory
# MySQLdb settings
MySQL=False
#Mydb     ="OGNDB"
#Myuser   ="ogn"
#Mypasswd ="ogn"
#Myhost   ="ubuntu" 
# --------------------------------------#
DBhost   =socket.gethostname()
DBuser   ="ogn"
DBpasswd ="ogn"
DBname   ="APRSLOG"
# --------------------------------------#
