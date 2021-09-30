#!/bin/bash

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
dir=$DBpath
cd $dir
echo "......"$(hostname)"........." 		
date                   				
python3 ~/src/SARsrc/SARcalsunrisesunset.py 
python3 ~/src/SARsrc/SARognES.py           
