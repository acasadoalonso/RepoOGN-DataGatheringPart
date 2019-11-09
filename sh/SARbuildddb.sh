#!/bin/sh
echo "Build GLIDERS table: "
cd /nfs/OGN/src/SARsrc/flarmdb
ls -la
if [ $# -eq  0 ]; then
	server='localhost'
	server2='localhost'
else
	server=$1
	server2='localhost'
fi
echo "Server: "$server
if [ $#  -gt  1 ]; then
	server2=$2
fi
echo "Server2: "$server2
#server="ubuntu"
#server2="casadonfs"
rm *.fln 2>/dev/null
rm *.csv 2>/dev/null
rm *.txt 2>/dev/null
wget -o flarmdata.log  www.flarmnet.org/static/files/wfn/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1
python3 ognbuildfile.py 
python3 flarmbuildfile.py 
echo "# $(date +%F) $(hostname) " >TTTbuilt
cat flarm.hdr flarmdata.txt  >flarmdata.py 
cat ogn.hdr   ognddbdata.txt >ognddbdata.py 
cat TTTbuilt kglid.hdr ognddbdata.py  flarmdata.py kglid.trail >kglid.py
rm             kglid.bkup
mv ../kglid.py kglid.bkup
cp kglid.py ../
cp kglid.py ../..
cp kglid.py /var/www/html/
cp kglid.py /nfs/OGN/DIRdata
rm *.fln
rm *.txt
rm *.csv
rm flarmdata.py ognddbdata.py
ls -la
cd /nfs/OGN/DIRdata
echo "Registered gliders: "
echo "select count(*) from GLIDERS;" |                sqlite3 SAROGN.db
echo "drop table GLIDERS;"           |                mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
echo "Copy from sqlite3 to MySQL OGNDB: "$server
sqlite3 SAROGN.db ".dump GLIDERS" | python2 ../src/SARsrc/sql* | mysql --login-path=SARogn -h $server OGNDB  	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
echo "Copy from sqlite3 to MySQL APRSLOG: "$server
echo "delete from GLIDERS;"           |                mysql --login-path=SARogn -h $server APRSLOG 		2>/dev/null
#sqlite3 SAROGN.db ".dump GLIDERS" | python2 ../src/SARsrc/sql* | mysql --login-path=SARogn -h $server APRSLOG	2>/dev/null
mysql --login-path=SARogn -h $server APRSLOG < ~/src/SARsrc/sh/copyGLIDERS.sql 					2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql --login-path=SARogn -h $server APRSLOG 		2>/dev/null
echo "Copy from sqlite3 to MySQL SWIFACE: "$server2 
echo "drop table GLIDERS;"           |                mysql --login-path=SARogn -h $server2 SWIFACE 		2>/dev/null
sqlite3 SAROGN.db ".dump GLIDERS" | python2 ../src/SARsrc/sql* | mysql --login-path=SARogn -h $server2 SWIFACE 	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql --login-path=SARogn -h $server2 SWIFACE 		2>/dev/null

cd 
