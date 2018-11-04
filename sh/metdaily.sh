#!/bin/sh
PATHSRC=/nfs/OGN/src
DBHOST=UBUNTU
cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      		>>metar$(date +%y%m%d).log
echo "==============="        		>>metar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>fcst$(date  +%y%m%d).log
echo "==============="        		>>fcst$(date  +%y%m%d).log
sqlite3 METEO.db ".dump METEO" >meteo.dmp
python $PATHSRC/sql*                    <meteo.dmp  >meteo.sql
sed "s/CREATE TABLE/-- CREATE TABLE/g" meteo.sql | sed "s/CREATE UNIQUE INDEX/-- CREATE INDEX/g" | mysql -u ogn -pogn -h $DBHOST OGNDB 
python $PATHSRC/ogndb/DBmeteo.py      	>>metar$(date +%y%m%d).log
mv metar*.log log/
mv fcst*.log  log/
mv meteo.sql meteo.dmp tmp
cd 
