cd /nfs/OGN/DIRdata
mv SARgetogn.log log/SARgetogn$(date +%y%m).log
mv SARerr.log    log/SARerr$(date    +%y%m).log
rm        db/OGN.BKUP.db
cp OGN.db db/OGN.BKUP.db
sqlite3 OGN.db "vacuum;"
cd  log
mv *$(date +%y)*.log Y$(date +%y) 
bash ./compress.sh   Y$(date +%y) 
cd
