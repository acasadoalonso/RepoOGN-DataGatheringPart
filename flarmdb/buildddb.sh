#!/bin/bash
# source the config file 
#eval "$(egrep "^[^ ]*=[^;&]*'" ../config.py )"
DBpath=/nfs/OGN/DIRdata/
SQLite3=SAROGN.db
echo "DB: "$DBpath$SQLite3
cd /var/www/html/flarmdb
rm *.fln 2>/dev/null
rm *.csv 2>/dev/null
rm *.txt 2>/dev/null
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
echo "ksta = { "                >>tttbuilt
cat ksta.hdr                    >>tttbuilt
cat kglid.trail                 >>tttbuilt
echo "kglid = { "               >>tttbuilt
cat flarm.hdr flarmdata.txt  >flarmdata.py 
cat ogn.hdr   ognddbdata.txt >ognddbdata.py 
cat tttbuilt ksta.hdr kglid.hdr ognddbdata.py  flarmdata.py kglid.trail >kglid.py
python3 kglid.py 
cp kglid.py /var/www/html/files 
cp kglid.py ../../
rm *.fln
rm *.csv
rm *.txt
rm *.log
rm flarmdata.py ognddbdata.py
ls -la
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3}
cd 
