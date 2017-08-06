#!/bin/sh
db='/var/www/DIRdata/OGN.db'
# test if DB is available
if [ ! -e $db ]
then
	logger -t $0 "DB mount seems down, restarting"
        sudo service rpcbind start
        sudo mount -t nfs casadonfs:/nfs/NFS/Documents/OGN/DIRdata /var/www/DIRdata
        sleep 10
fi

