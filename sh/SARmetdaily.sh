#!/bin/bash
if [ $# = 0 ]; then
	server='localhost'
else
	server=$1
fi

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )

cd $DBpath
echo "Server: "$server 			>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
echo "======"$(hostname)"=========" 	>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARfcst$(date  +%y%m%d).log
echo "======"$(hostname)"========="    	>>SARfcst$(date  +%y%m%d).log
sqlite3 SARMETEO.db ".dump METEO" >meteo.dmp
python3 ~/src/SARsrc/sqlite3-to-mysql.py  <meteo.dmp  >meteo.sql
sed "s/CREATE TABLE/-- CREATE TABLE/g" meteo.sql | sed "s/CREATE UNIQUE INDEX/-- CREATE INDEX/g" | mysql -u $DBuser -p$DBpasswd -h $server OGNDB  2>/dev/null
sqlite3 SARMETEO.db ".dump WX" >meteo.dmp
python3 ~/src/SARsrc/sqlite3-to-mysql.py  <meteo.dmp  >meteo.sql
sed "s/CREATE TABLE/-- CREATE TABLE/g" meteo.sql | sed "s/CREATE UNIQUE INDEX/-- CREATE INDEX/g" | mysql -u $DBuser -p$DBpasswd -h $server OGNDB  2>/dev/null
python3 ~/src/SARsrc/ogndb/DBmeteo.py 	>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
mv SARmet* log/
mv SARfcs* log/
if [[ -f SAR.alive ]]
then
   rm SAR.alive
fi
mv meteo.sql meteo.dmp tmp
cd 
