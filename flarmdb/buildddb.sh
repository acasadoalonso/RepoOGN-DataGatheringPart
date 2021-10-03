#!/bin/bash
#DBpath=/nfs/OGN/DIRdata/
#SQLite3=SAROGN.db
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi

DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
SQLite3=$(echo  `grep '^SQLite3 '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^SQLite3 //g' | sed 's/ //g' )
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH $DBpath $SQLite3 
cd $SCRIPTPATH

echo "DB: "$DBpath$SQLite3
rm *.fln 2>/dev/null
rm *.csv 2>/dev/null
rm *.txt 2>/dev/null
#wget -o flarmdata.log  www.flarmnet.org/files/data.fln
wget -o flarmdata.log  www.flarmnet.org/static/files/wfn/data.fln --no-check-certificate 
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
#wget -o ognddbdata.log localhost:82/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1
#wget -O ognddbdata.json -o ogndbjson.log localhost:82/download/?j=1
echo "Start gen the DB"
echo "================"
python3 ognbuildfile.py 
echo "Registered gliders from OGN DDB: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3} -echo
python3 flarmbuildfile.py 
echo "Registered gliders after FlarmNET: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3} -echo
echo "End of gen the DB ... "
echo
echo
rm *.fln
rm *.csv
rm *.txt
rm *.log
#ls -la
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" | sqlite3 ${DBpath}${SQLite3} -echo
cd 
