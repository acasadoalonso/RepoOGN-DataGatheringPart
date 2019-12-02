#!/bin/bash 
cd /nfs/OGN/DIRdata 
cp SAROGN.db db/SAROGN.Y$(date +%y).db
sqlite3 -echo SAROGN.db “delete from OGNDATA;”
sqlite3 -echo SAROGN.db "vacuum;"
mysql --login-path=SARogn -e "INSERT into OGNDBARCHIVE.METEO (SELECT * FROM OGNDB.METEO WHERE OGNDB.METEO.date < '$(date +%y)0000');"
mysql --login-path=SARogn -e "DELETE from OGNDB.METEO                                   WHERE OGNDB.METEO.date < '$(date +%y)0000' ;"
mysql --login-path=SARogn -e "INSERT into OGNDBARCHIVE.OGNDATA (SELECT * FROM OGNDB.OGNDATA WHERE OGNDB.OGNDATA.date < '$(date +%y)0000');"
mysql --login-path=SARogn -e "DELETE from OGNDB.OGNDATA                                     WHERE OGNDB.OGNDATA.date < '$(date +%y)0000' ;"
mkdir data/Y$(date +%y)
mkdir log/Y$(date +%y)
mkdir fd/Y$(date +%y)
cd
