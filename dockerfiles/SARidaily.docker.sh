#!/bin/bash
echo " "
server="mariadb"
hostname=$(hostname)
city=$1
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
cd $DBpath
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
echo "                   " 				>>SARproc.docker.log
echo "SAROGN: end of day process using MariaDB." 	>>SARproc.docker.log
echo "=========================================="	>>SARproc.docker.log
echo "                   " 				>>SARproc.docker.log
date			 				>>SARproc.docker.log
echo "                   " 				>>SARproc.docker.log
docker exec -it sarogn /bin/bash /var/www/SARpogn.docker.sh
docker stop sarogn 	 				>>SARproc.docker.log
echo "                   " 				>>SARproc.docker.log
mysqlcheck -u $DBuser -p$DBpasswd -h $server OGNDB   	>>SARproc.docker.log
mysqlcheck -u $DBuser -p$DBpasswd -h $server OGNDBARCHIVE 	>>SARproc.docker.log
echo "Set session ...     " 				>>SARproc.docker.log
echo "set session sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'; "| mysql   -v -h $server -u $DBuser -p$DBpasswd OGNDB	      						   >>SARproc.docker.log
echo "select 'Number of fixes: on the DB:', count(*) from OGNDATA; select station, 'Kms.max.:',max(distance),'        Flarmid :',idflarm, 'Date:',date, time, station from OGNDATA group by station; "  | mysql   -v -h $server -u $DBuser -p$DBpasswd OGNDB	   >>SARproc.docker.log
echo "mysqldump  ...       " 				>>SARproc.docker.log
mysqldump  -u $DBuser -p$DBpasswd --add-drop-table -h $server OGNDB OGNDATA >ogndata.sql 
mysql      -u $DBuser -p$DBpasswd                  -h $server OGNDBARCHIVE  <ogndata.sql 	>>SARproc.docker.log
echo "delete from OGNDATA ...  " 								>>SARproc.docker.log
echo "delete from OGNDATA;" | mysql -u $DBuser -p$DBpasswd     -v -h $server OGNDB       	>>SARproc.docker.log
mv ogndata.sql archive
docker logs --timestamps --details --since $(date +%Y-%m-%d) sarogn 				>>SARproc.docker.log
echo "End of processes  MariaDB at server: "$hostname $(date) $HOSTNAME $city			>>SARproc.docker.log
echo "=========================================================================="		>>SARproc.docker.log
mv SARproc.docker.log archive/SARiproc.docker$(date +%y%m%d).log
cd
