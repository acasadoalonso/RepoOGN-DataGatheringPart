#!/bin/bash
if [ $# = 0 ]; then
	server='localhost'
else
	server=$1
fi

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g')
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )

cd $DBpath
echo "DBpath: "$DBpath
echo $(hostname)" for Server: "$server >>SARgetogn.log 
mv SARgetogn.log log/SARgetogn$(date +%y%m).log
mv SARerr.log    log/SARerr$(date    +%y%m).log
sqlite3 -echo SAROGN.db "delete from receivers where idrec like 'FNB%'; " 
sqlite3 -echo SAROGN.db "delete from receivers where idrec like 'XCG%'; " 
sqlite3 -echo SAROGN.db "delete from receivers where idrec like 'XCG%'; " 
sqlite3 -echo SAROGN.db "delete from receivers where idrec like 'BSKY%'; " 
sqlite3 -echo SAROGN.db "vacuum;"
rm        db/SAROGN.BKUP.db
cp SAROGN.db db/SAROGN.BKUP.db
echo "delete from RECEIVERS where idrec like 'FNB%';"  |  mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'XCG%';"  |  mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'XCG%';"  |  mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'BSKY%';" |  mysql -u $DBuser -p$DBpasswd -h $server OGNDB 		2>/dev/null
cd  log
mv *$(date +%y)*.log Y$(date +%y) 
bash ./compress.sh   Y$(date +%y) 
cd ../
pwd
bash fd/compfull.sh 
sudo chown $USER:www-data -R fd
cd
