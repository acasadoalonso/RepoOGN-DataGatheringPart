#!/bin/sh
cd /nfs/OGN/src/SARsrc/flarmdb
server="ubuntu"
server2="casadonfs"
rm *.fln
rm *.csv
wget -o flarmdata.log  www.flarmnet.org/static/files/wfn/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1
python ognbuildfile.py 
python flarmbuildfile.py 
echo "# $(date +%F) $(hostname) " >TTTbuilt
cat flarmhdr flarmdata.txt  >flarmdata.py 
cat ognhdr   ognddbdata.txt >ognddbdata.py 
cat TTTbuilt kglidhdr ognddbdata.py  flarmdata.py kglidtrail >kglid.py
rm             kglid.bkup
mv ../kglid.py kglid.bkup
cp kglid.py ../
cp kglid.py /var/www/html/
cp kglid.py /nfs/OGN/DIRdata
ls -la
cd /nfs/OGN/DIRdata
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" |                sqlite3 OGN.db
echo "drop table GLIDERS;"           |                mysql -h $server -u ogn -pogn OGNDB 		2>/dev/null
sqlite3 OGN.db ".dump GLIDERS" | python ../src/SARsrc/sql* | mysql -h $server -u ogn -pogn OGNDB  	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn OGNDB 		2>/dev/null
echo "delete from GLIDERS;"           |                mysql -h $server -u ogn -pogn APRSLOG 		2>/dev/null
#sqlite3 OGN.db ".dump GLIDERS" | python ../src/sql* | mysql -h $server -u ogn -pogn APRSLOG  		2>/dev/null
mysql -h $server -u ogn -pogn APRSLOG < ~/src/SARsrc/copyGLIDERS.sql 					2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn APRSLOG 		2>/dev/null
echo "drop table GLIDERS;"           |                mysql -h $server2 -u ogn -pogn SWIFACE 		2>/dev/null
sqlite3 OGN.db ".dump GLIDERS" | python ../src/SARsrc/sql* | mysql -h $server2 -u ogn -pogn SWIFACE  	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -h $server2 -u ogn -pogn SWIFACE 		2>/dev/null
cd 
