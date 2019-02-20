#!/bin/sh
cd /nfs/OGN/src/flarmdb
hn=$(hostname)
if [ $hn = 'SAROGN' ]
then
	server="ubuntu"
	server2="casadonfs"
else
	server="localhost"
	server2="localhost"
fi
echo $server $server2
rm *.fln
rm *.csv
wget -o flarmdata.log  www.flarmnet.org/static/files/wfn/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1
python ognbuildfile.py 
echo "Registered OGN gliders: "
echo "select count(*) from GLIDERS;" |                sqlite3 /nfs/OGN/DIRdata/OGN.db
python flarmbuildfile.py 
echo "select count(*) from GLIDERS;" |                sqlite3 /nfs/OGN/DIRdata/OGN.db
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
echo "drop table GLIDERS;"           |                mysql -h $server -u ogn -pogn OGNDB
sqlite3 OGN.db ".dump GLIDERS" | python ../src/sql* | mysql -h $server -u ogn -pogn OGNDB 
echo "ALTER TABLE OGNDB.GLIDERS ADD PRIMARY KEY (idglider) USING BTREE;;"  | mysql -h $server -u ogn -pogn OGNDB
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn OGNDB
echo "delete from GLIDERS;"           |                mysql -h $server -u ogn -pogn APRSLOG
#sqlite3 OGN.db ".dump GLIDERS" | python ../src/sql* | mysql -h $server -u ogn -pogn APRSLOG 
mysql -h $server -u ogn -pogn APRSLOG < ~/src/SARsrc/sh/copyGLIDERS.sql
#echo "ALTER TABLE APRSLOG.GLIDERS ADD PRIMARY KEY (idglider) USING BTREE;;"  | mysql -h $server -u ogn -pogn APRSLOG
echo "select count(*) from GLIDERS;" |                mysql -h $server -u ogn -pogn APRSLOG
echo "drop table GLIDERS;"           |                mysql -h $server2 -u ogn -pogn SWIFACE
#echo "ALTER TABLE SWIFACE.GLIDERS ADD PRIMARY KEY (idglider) USING BTREE;;"  | mysql -h $server -u ogn -pogn SWIFACE
sqlite3 OGN.db ".dump GLIDERS" | python ../src/sql* | mysql -h $server2 -u ogn -pogn SWIFACE 
echo "select count(*) from GLIDERS;" |                mysql -h $server2 -u ogn -pogn SWIFACE
cd 
