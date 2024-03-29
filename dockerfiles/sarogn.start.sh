#!/bin/bash
# include the call to this scipt on the crontab

if [ $# = 0 ]; then
        city='Madrid'
else
        city=$1
fi

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi

DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
location=$(echo  `grep '^location_name '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^location_name //g' | sed 's/ //g' )
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
#echo $SCRIPTPATH
cd $DBpath
echo "Starting docker container sarogn at: "$HOSTNAME $(date) 				>>SARproc.docker.log
echo "================================================================================"	>>SARproc.docker.log
echo "Location: "$location "City: "$city 						>>SARproc.docker.log
if [ ! "$(docker ps -q -f name=sarogn)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=sarogn)" ]; then
        echo "Starting an existing exited container sarogn ..."				>>SARproc.docker.log
        docker restart sarogn								>>SARproc.docker.log 2>&1
    else
        echo "Starting a new container sarogn ..."					>>SARproc.docker.log
        bash $SCRIPTPATH/sarogn.sh							>>SARproc.docker.log
    fi
else
    echo "Starting an existing container sarogn ..."					>>SARproc.docker.log
    docker restart sarogn								>>SARproc.docker.log 2>&1
fi
docker exec -it sarogn python3 /var/www/main/SARcalsunrisesunset.py			>>SARproc.docker.log
docker ps -a										>>SARproc.docker.log
/bin/echo '/bin/bash ~/src/SARsrc/dockerfiles/SARidaily.docker.sh '$city | at -M $(/usr/local/bin/calcelestial -n -p sun -m set -q $city ) - 25 minutes  >>SARproc.docker.log 2>&1
echo "Container scheduled ... at: $(date) "						>>SARproc.docker.log
echo " "										>>SARproc.docker.log
echo "=============================================================================== "	>>SARproc.docker.log
