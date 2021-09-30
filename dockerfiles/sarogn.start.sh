#!/bin/bash
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
location=$(echo  `grep '^location_name '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^location_name //g' | sed 's/ //g' )
cd $DBpath
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
city='Madrid'
echo "Starting docker container sarogn at: "$HOSTNAME $(date) 				>>SARproc.docker.log
echo "================================================================================"	>>SARproc.docker.log
echo "Location: "$location "City: "$city 						>>SARproc.docker.log
docker start sarogn 									>>SARproc.docker.log
docker exec -it sarogn python3 /var/www/main/SARcalsunrisesunset.py			>>SARproc.docker.log
/bin/echo '/bin/bash ~/src/SARsrc/dockerfiles/SARidaily.docker.sh '$city | at -M $(calcelestial -n -p sun -m set -q $city )  >>SARproc.docker.log 2>&1
echo "Container scheduled ..."								>>SARproc.docker.log
