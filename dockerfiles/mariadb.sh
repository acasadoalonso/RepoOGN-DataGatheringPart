#!/bin/bash
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi

DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )

docker run --net mynetsql --ip 172.18.0.2 --restart unless-stopped --name mariadb -e MYSQL_ROOT_PASSWORD=$DBpasswd -d mariadb/server:10.4 --log-bin --binlog-format=MIXED 


