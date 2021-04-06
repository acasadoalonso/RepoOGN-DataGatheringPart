#!/bin/bash
echo "Build GLIDERS table from server: "$(hostname)
echo "============================================================================================================================================="
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

DBuser=$(echo  `grep '^DBuser' /etc/local/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser//g')
DBpasswd=$(echo  `grep '^DBpasswd' /etc/local/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd//g' | sed 's/ //g' )

rm *.fln 2>/dev/null
rm *.csv 2>/dev/null
rm *.txt 2>/dev/null
wget -o flarmdata.log  --no-check-certificate www.flarmnet.org/static/files/wfn/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
wget -O ognddbdata.json -o ogndbjson.log ddb.glidernet.org/download/?j=1

python3 ognbuildfile.py 
python3 flarmbuildfile.py 

rm *.fln
rm *.txt
rm *.csv
rm *.log
echo "Table GLIDERS on SAROGN.db done ..."
cd /nfs/OGN/DIRdata
echo
echo "Build the MySQL databases on the servers:"
echo
echo "Server:  "$server
echo "Server2: "$server2
echo "Registered gliders from sqlite3: "
echo "select count(*) from GLIDERS;" |                sqlite3 -echo SAROGN.db
echo "drop table GLIDERS;"           |                mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
echo "Copy from sqlite3 to MySQL OGNDB: "$server
sqlite3 SAROGN.db ".dump GLIDERS" | python3 ~/src/SARsrc/sqlite3-to-mysql.py | mysql -u $DBuser -p$DBpasswd  OGNDB	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
echo "Copy from sqlite3 to MySQL APRSLOG: "$server
echo "delete from GLIDERS;"           |                mysql -u $DBuser -p$DBpasswd -h $server APRSLOG 		2>/dev/null
#sqlite3  SAROGN.db ".dump GLIDERS" | python3 ~/src/SARsrc/sqlite3-to-mysql.py | mysql -u $DBuser -p$DBpasswd APRSLOG	2>/dev/null
mysql -u $DBuser -p$DBpasswd -h $server APRSLOG < ~/src/SARsrc/sh/copyGLIDERS.sql 					2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -u $DBuser -p$DBpasswd -h $server APRSLOG 		2>/dev/null
echo "Copy from sqlite3 to MySQL SWIFACE: "$server2 
echo "drop table GLIDERS;"           |                mysql -u $DBuser -p$DBpasswd -h $server2 SWIFACE 		2>/dev/null
sqlite3 SAROGN.db ".dump GLIDERS" | python3 ~/src/SARsrc/sqlite3-to-mysql.py | mysql -u $DBuser -p$DBpasswd -h $server2 SWIFACE 	2>/dev/null
echo "select count(*) from GLIDERS;" |                mysql -u $DBuser -p$DBpasswd -h $server2 SWIFACE 		2>/dev/null
mysqldump -u $DBuser -p$DBpasswd -h $server --add-drop-table OGNDB GLIDERS                                       >/var/www/html/files/GLIDERS.sql  
if [[ $(hostname) == 'CasadoUbuntu' ]]
then
	echo "Update MariaDB"
	mysql --defaults-extra-file=~/.mariadb APRSLOG                                                                  </var/www/html/files/GLIDERS.sql  
	mysql --defaults-extra-file=~/.mariadb OGNDB                                                                    </var/www/html/files/GLIDERS.sql  
	mysql --defaults-extra-file=~/.mariadb SWIFACE                                                                  </var/www/html/files/GLIDERS.sql  
fi
echo "============================================================================================================================================="
cd 
