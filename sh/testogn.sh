#!/bin/bash
ss=$(/usr/local/bin/calcelestial -p sun -m set -q Madrid -H civil -f %s)
now=$(date +%s)
let "dif=$ss-$now"
if [ $dif -lt 0 ]
then 
	logger  -t $0 "OGN Repo Nothing to do: "$dif" Now: "$now" Sunset: "$ss
else 
	pgrep python
	if [ $? -ne 0 ] # if OGN repo interface is  not running
	then
#               restart SWS
    		sh /home/pi/src/boot_flight_logger.sh
    		logger -t $0 "OGN repo seems down, restarting"
	else
    		logger -t $0 "OGN repo seems up: "$dif" Now: "$now" Sunset: "$ss
	fi
fi
