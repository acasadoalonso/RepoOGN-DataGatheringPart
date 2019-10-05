#!/bin/bash 
cd /nfs/OGN/DIRdata 
cp SAROGN.db db/SAROGN.Y$(date +%y).db
sqlite3 SAROGN.db “delete from OGNDATA;”
sqlite3 SAROGN.db "vacuum;"
mkdir data/Y$(date +%y)
mkdir log/Y$(date +%y)
mkdir fd/Y$(date +%y)
cd
