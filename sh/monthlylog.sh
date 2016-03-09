cd /nfs/OGN/DIRdata
mv getogn.log log/getogn$(date +%m%y).log
mv err.log  log/err$(date +%m%y).log
rm        tmp/OGN.BKUP.db
cp OGN.db tmp/OGN.BKUP.db
sqlite3 OGN.db "vacuum;"
cd  log
mv *$(date +%y%m)*.log Y$(date +%y) 
cd
