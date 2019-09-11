#!/bin/bash
# source the config file 
#eval "$(egrep "^[^ ]*=[^;&]*'" ../config.py )"
DBpath=/nfs/OGN/DIRdata/
SQLite3=OGN.db
echo "DB: "$DBpath$SQLite3
cd /var/www/html/flarmdb
rm *.fln
rm *.csv
#wget -o flarmdata.log  www.flarmnet.org/files/data.fln
wget -o flarmdata.log  www.flarmnet.org/static/files/wfn/data.fln --no-check-certificate 
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1
echo "Start gen the DB"
python3 ognbuildfile.py 
echo "Registered gliders OGN: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3}
python3 flarmbuildfile.py 
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3}
echo "End of gen the DB"
echo "# $(date +%F) $(hostname)" >tttbuilt
cat flarmhdr flarmdata.txt  >flarmdata.py 
cat ognhdr   ognddbdata.txt >ognddbdata.py 
cat tttbuilt kglidhdr ognddbdata.py  flarmdata.py kglidtrail >kglid.py
ls -la
cp kglid.py /var/www/html/files 
cp kglid.py ../../
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3}
cd 
