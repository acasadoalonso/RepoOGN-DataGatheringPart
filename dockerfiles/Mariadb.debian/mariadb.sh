#!/bin/bash
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
if [ -f $CONFIGDIR/SARconfig.ini ]
then
   DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
   DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
   DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
else
   DBuser='ogn'
   DBpasswd='ogn'
fi
   
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

docker run --net mynetsql --ip 172.18.0.2 --name mariadb --restart unless-stopped -e MYSQL_ROOT_PASSWORD=$DBpasswd -d mariadb:latest 


