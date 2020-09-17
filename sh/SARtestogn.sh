#!/bin/bash
sunsetfile=$"/nfs/OGN/DIRdata/SAR.sunset"
alive=$"/nfs/OGN/DIRdata/SAR.alive"
pid=$"/tmp/SAR.pid"
hn=`hostname   `
if [ $# = 0 ]; then
	city='Madrid'
else
	city=$1
fi
if [ -f $sunsetfile ]
        then
                ss=$(cat $sunsetfile)
        else
                ss=$(/usr/local/bin/calcelestial -p sun -m set -q $city -H civil -f %s)
fi
now=$(date +%s)
let "dif=$ss-$now"
if [ $dif -lt 0 ]
then 
	logger  -t $0 "OGN Repo Nothing to do: "$dif" Now: "$now" Sunset: "$ss
else 
	if [ ! -f $alive ]
	then
		logger  -t $0 "OGN Repo is not alive "$hn
                if [ -f $pid ] # if OGN repo interface is  not running
                then
                        sudo kill $(cat /tmp/SAR.pid)
                fi
#               restart OGN data collector
    		bash ~/src/SARsrc/sh/SARboot_flight_logger.sh $city
    		logger -t $0 "OGN repo seems down, restarting "$hn
		echo $(date)" - "$(hostname) >>/nfs/OGN/DIRdata/.SARrestart.log 
	else
    		logger -t $0 $hn" OGN repo seems up: "$dif" Now: "$now" Sunset: "$ss" at: "$city
	fi
fi

if [ -f $alive ]
then
		rm $alive
fi
