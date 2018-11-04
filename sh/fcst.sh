#!/bin/sh
PATHSRC=/nfs/OGN/src
cd /nfs/OGN/DIRdata
python $PATHSRC/fcst.py     >>fcst$(date +%y%m%d).log
echo $(date +%H:%M:%S)      >>fcst$(date +%y%m%d).log
echo "============="        >>fcst$(date +%y%m%d).log
/bin/echo '/bin/sh $PATHSRC/fcst.sh' | at -M $(date +%H:%M)+ 6 hours
cd 
