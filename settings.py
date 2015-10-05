
#-------------------------------------
# OGN-Flight-Logger Settings
#-------------------------------------
# Python APRS/OGN program to log flight times, durations and maximum heights achieved
#
#
#-------------------------------------
# Setting values
#-------------------------------------
#

APRS_SERVER_HOST = 'aprs.glidernet.org'
APRS_SERVER_PORT = 14580
APRS_USER = 'SpainW'
# APRS_PASSCODE = -1   #Read only

APRS_PASSCODE = 12204  							# See http://www.george-smart.co.uk/wiki/APRS_Callpass
APRS_FILTER_DETAILS = "filter r/+39.71498/-3.31366/620\n " 		# LELT center and covering Spain (Lillo-->Portbou)
									# Check that APRS_USER and APRS_PASSCODE are set
assert len(APRS_USER) > 3 and len(str(APRS_PASSCODE)) > 0, 'Please set APRS_USER and APRS_PASSCODE in settings.py.'
									# aprs.glidernet.org on port 14580.
FLOGGER_DB_SCHEMA = "flogger_schema-0.0.1.sql"
FLOGGER_LATITUDE, FLOGGER_LONGITUDE = '+39.71498', '-3.31366'
FLOGGER_MIN_FLIGHT_TIME = "0:5:0" 					#hh:mm:ss
FLOGGER_KEEPALIVE_TIME = 900 						# Interval in seconds for sending tcp/ip keep alive on socket connection
