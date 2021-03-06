#!/bin/bash

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
if [ $# = 0 ]; then
	city='Madrid'
else
	city=$1
fi

cd $DBpath
echo "......"$(hostname)"........." 		>>SARgetogn.log 
date                   				>>SARgetogn.log 
calcelestial -p sun -m set -q $city -H civil 	>>SARgetogn.log 
echo "......"$(hostname)"........." 		>>SARerr.log 
date                   				>>SARerr.log 
calcelestial -p sun -m set -q $city -H civil 	>>SARerr.log 
echo "......"$(hostname)"........." 		>>SARerr.log 
python3 ~/src/SARsrc/SARcalsunrisesunset.py 	>>SARgetogn.log
python3 ~/src/SARsrc/SARognES.py             	>>SARgetogn.log  2>>SARerr.log &
cd
