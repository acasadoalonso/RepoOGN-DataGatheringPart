#!/bin/bash
if [ $# = 0 ]; then
	city='lemd'
else
	city=$1
fi

cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)                 >>SARmetar$(date +%y%m%d).log
echo "============="                   >>SARmetar$(date +%y%m%d).log
python3 ../src/SARsrc/SARmeteo-$city.py >>SARmetar$(date +%y%m%d).log
echo "======"$(hostname)"======="      >>SARmetar$(date +%y%m%d).log
cd 
