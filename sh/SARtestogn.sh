#!/bin/bash
sunsetfile=$"/nfs/OGN/DIRdata/SAR.sunset"
alive=$"/nfs/OGN/DIRdata/SAR.alive"
if [ -f $sunsetfile ]
        then
                ss=$(cat $sunsetfile)
        else
                city='Madrid'
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
		logger  -t $0 "OGN Repo is not alive"
		pnum=$(pgrep python3)
		if [ $? -eq 0 ] # if OGN repo interface is  not running
		then
			sudo kill $pnum
		fi
#               restart OGN data collector
    		sh ~/src/SARsrc/sh/SARboot_flight_logger.sh
    		logger -t $0 "OGN repo seems down, restarting"
		date >>/nfs/OGN/DIRdata/.restart.log 
	else
    		logger -t $0 "OGN repo seems up: "$dif" Now: "$now" Sunset: "$ss
	fi
fi

if [ -f $alive ]
        then
		rm $alive
fi
