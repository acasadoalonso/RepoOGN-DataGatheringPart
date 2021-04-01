#!/bin/bash 
cd /nfs/OGN/DIRdata 

DBuser=$(echo  `grep '^DBuser' /etc/local/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser//g')
DBpasswd=$(echo  `grep '^DBpasswd' /etc/local/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd//g' | sed 's/ //g' )
echo "-u "$DBuser" --password="$DBpasswd

cp SAROGN.db db/SAROGN.Y$(date +%y).db
sqlite3 -echo SAROGN.db "delete from OGNDATA;"
sqlite3 -echo SAROGN.db "vacuum;"
mysql -u $DBuser -p$DBpasswd -e "INSERT into OGNDBARCHIVE.METEO (SELECT * FROM OGNDB.METEO WHERE OGNDB.METEO.date < '$(date +%y)0000');"
mysql -u $DBuser -p$DBpasswd -e "DELETE from OGNDB.METEO                                   WHERE OGNDB.METEO.date < '$(date +%y)0000' ;"
mysql -u $DBuser -p$DBpasswd -e "INSERT into OGNDBARCHIVE.OGNDATA (SELECT * FROM OGNDB.OGNDATA WHERE OGNDB.OGNDATA.date < '$(date +%y)0000');"
mysql -u $DBuser -p$DBpasswd -e "DELETE from OGNDB.OGNDATA                                     WHERE OGNDB.OGNDATA.date < '$(date +%y)0000' ;"
mkdir -p data/Y$(date +%y)
mkdir -p log/Y$(date +%y)
mkdir -p fd/Y$(date +%y)
cd
