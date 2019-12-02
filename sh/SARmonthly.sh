#!/bin/bash
if [ $# = 0 ]; then
	server='localhost'
else
	server=$1
fi

cd /nfs/OGN/DIRdata
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
echo "delete from RECEIVERS where idrec like 'FNB%';"  |  mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'XCG%';"  |  mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'XCG%';"  |  mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
echo "delete from RECEIVERS where idrec like 'BSKY%';" |  mysql --login-path=SARogn -h $server OGNDB 		2>/dev/null
cd  log
mv *$(date +%y)*.log Y$(date +%y) 
bash ./compress.sh   Y$(date +%y) 
cd ../
pwd
bash fd/compfull.sh 
cd
