#!/bin/sh
PATHSRC=/nfs/OGN/src
cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      		>>dbdump$(date +%y%m%d-%H).log
echo "============="        		>>dbdump$(date +%y%m%d-%H).log
python $PATHSRC/ogndb/DBdump.py LNAMES 	>>dbdump$(date +%y%m%d-%H).log
echo $(date +%H:%M:%S)      		>>dbdump$(date +%y%m%d-%H).log
echo "============="        		>>dbdump$(date +%y%m%d-%H).log
cd 
