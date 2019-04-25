cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
echo "==============="        		>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARfcst$(date  +%y%m%d).log
echo "==============="        		>>SARfcst$(date  +%y%m%d).log
sqlite3 METEO.db ".dump METEO" >meteo.dmp
python ../src/sql*             <meteo.dmp  >meteo.sql
sed "s/CREATE TABLE/-- CREATE TABLE/g" meteo.sql | sed "s/CREATE UNIQUE INDEX/-- CREATE INDEX/g" | mysql -u ogn -pogn -h ubuntu OGNDB  2>/dev/null
python ../src/ogndb/DBmeteo.py        	>>SARmetar$(date +%y%m%d).log
mv SARmet* log/
mv SARfcs* log/
mv meteo.sql meteo.dmp tmp
cd 
