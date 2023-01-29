#!/bin/bash 

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
mkdir -p data/Y$(date +%y)
mkdir -p log/Y$(date +%y)
mkdir -p fd/Y$(date +%y)
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
DBhost=$(echo    `grep '^DBhost '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBhost //g' | sed 's/ //g' )
cd $DBpath
cp SAROGN.db db/SAROGN.Y$(date +%y).db
sqlite3 -echo SAROGN.db "delete from OGNDATA;"
sqlite3 -echo SAROGN.db "vacuum;"
mysql -h $DBhost -u $DBuser -p$DBpasswd -e "INSERT into OGNDBARCHIVE.METEO (SELECT * FROM OGNDB.METEO WHERE OGNDB.METEO.date < '$(date +%y)0000');"
mysql -h $DBhost -u $DBuser -p$DBpasswd -e "DELETE from OGNDB.METEO                                   WHERE OGNDB.METEO.date < '$(date +%y)0000' ;"
mysql -h $DBhost -u $DBuser -p$DBpasswd -e "INSERT into OGNDBARCHIVE.OGNDATA (SELECT * FROM OGNDB.OGNDATA WHERE OGNDB.OGNDATA.date < '$(date +%y)0000');"
mysql -h $DBhost -u $DBuser -p$DBpasswd -e "DELETE from OGNDB.OGNDATA                                     WHERE OGNDB.OGNDATA.date < '$(date +%y)0000' ;"
cd
