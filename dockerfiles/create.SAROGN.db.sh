#!/bin/bash
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

echo "Create the MySQL database OGNDB "											#
echo "Type the PASSword for the MySQL database OGNDB "									#
echo "================================================" 								#
echo "CREATE DATABASE  if not exists OGNDB " | mysql -h mariadb -u root -p$DBpasswd					#
mysql -h mariadb -u root -p$DBpasswd --database OGNDB < ../ogndb//DBschema.sql						#
echo "Create the MySQL OGN user "											#
sudo mysql -h mariadb -u root -p$DBpasswd <../doc/adduser.sql    								#
echo " "														#

