#!/bin/bash

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
dir=$DBpath
# test if directory is available
if [ ! -d $dir ]
then
#       sleep 2 mins for the NFS to start up
	#sudo service rpcbind start
	sudo mount casadonfs:/nfs/NFS/Documents /nfs
	sleep 120 
fi
cd $dir
echo "......"$(hostname)"........." >>SARgetogn.log 
date                   >>SARgetogn.log 
echo "......"$(hostname)"........." >>SARerr.log 
date                   >>SARerr.log 
python3 ~/src/SARsrc/SARcalsunrisesunset.py >>SARgetogn.log
python3 ~/src/SARsrc/SARognES.py            >>SARgetogn.log  2>>SARerr.log &
cd
