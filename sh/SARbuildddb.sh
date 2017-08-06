#!/bin/sh
cd /nfs/OGN/src/flarmdb
server="ubuntu"
rm *.fln
rm *.csv
wget -o flarmdata.log  www.flarmnet.org/files/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
python ognbuildfile.py 
python flarmbuildfile.py 
cat flarmhdr flarmdata.txt  >flarmdata.py 
cat ognhdr   ognddbdata.txt >ognddbdata.py 
cat kglidhdr ognddbdata.py  flarmdata.py kglidtrail >kglid.py
rm             kglid.bkup
mv ../kglid.py kglid.bkup
cp kglid.py ../
ls -la
cd /nfs/OGN/DIRdata
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" |                sqlite3 OGN.db
echo "drop table GLIDERS;"           |                mysql -h $server -u ogn -pogn OGNDB
sqlite3 OGN.db ".dump GLIDERS" | python ../src/sql* | mysql -h $server -u ogn -pogn OGNDB 
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn OGNDB
mysql -h $server -u ogn -pogn APRSLOG < ~/src/copyGLIDERStable.sql
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn APRSLOG
cd 
