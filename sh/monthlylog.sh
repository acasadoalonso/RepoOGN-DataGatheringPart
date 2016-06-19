cd /nfs/OGN/DIRdata
mv getogn.log log/getogn$(date +%m%y).log
mv err.log    log/err$(date    +%m%y).log
rm        db/OGN.BKUP.db
cp OGN.db db/OGN.BKUP.db
sqlite3 OGN.db "vacuum;"
cd  log
mv *$(date +%y)*.log Y$(date +%y) 
cd
