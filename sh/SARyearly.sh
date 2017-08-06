#!/bin/bash 
cd /nfs/OGN/DIRdata 
cp OGN.db db
sqlite3 OGN.db "vacuum;"
cd
