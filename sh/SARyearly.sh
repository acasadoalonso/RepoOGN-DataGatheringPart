#!/bin/bash 
cd /nfs/OGN/DIRdata 
cp OGN.db db/OGN.Y$(date +%y).db
sqlite3 OGN.db “delete from OGNDATA;”
sqlite3 OGN.db "vacuum;"
mkdir data/Y$(date +%y)
mkdir log/Y$(date +%y)
mkdir fd/Y$(date +%y)
cd
