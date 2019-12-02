#!/bin/bash
if [ $# = 0 ]; then
	server='localhost'
else
	server=$1
fi

cd /nfs/OGN/DIRdata
echo "Server: "$server 			>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
echo "======"$(hostname)"=========" 	>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARfcst$(date  +%y%m%d).log
echo "======"$(hostname)"========="    	>>SARfcst$(date  +%y%m%d).log
sqlite3 SARMETEO.db ".dump METEO" >meteo.dmp
python3 ../src/SARsrc/sql*             <meteo.dmp  >meteo.sql
sed "s/CREATE TABLE/-- CREATE TABLE/g" meteo.sql | sed "s/CREATE UNIQUE INDEX/-- CREATE INDEX/g" | mysql --login-path=SARogn -h $server OGNDB  2>/dev/null
python3 ../src/SARsrc/ogndb/DBmeteo.py        	>>SARmetar$(date +%y%m%d).log
mv SARmet* log/
mv SARfcs* log/
mv meteo.sql meteo.dmp tmp
cd 
