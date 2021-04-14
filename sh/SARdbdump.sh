#!/bin/bash
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )

cd $DBpath
echo $(date +%H:%M:%S)      		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "============="        		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "====="$(hostname)"========"	>>log/SARdbdump$(date +%y%m%d-%H).log
python3 ~/src/SARsrc/ogndb/DBdump.py  	>>log/SARdbdump$(date +%y%m%d-%H).log
echo $(date +%H:%M:%S)      		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "============="        		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "====="$(hostname)"========"	>>log/SARdbdump$(date +%y%m%d-%H).log
cd 
