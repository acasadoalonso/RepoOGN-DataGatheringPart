#!/bin/sh

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
db=$DBpath'/SAROGN.db'
# test if DB is available
if [ ! -e $db ]
then
	logger -t $0 "DB mount seems down, restarting"
        sudo service rpcbind start
        sudo mount -t nfs casadonfs:/nfs/NFS/Documents/OGN/DIRdata /var/www/DIRdata
        sleep 10
fi

