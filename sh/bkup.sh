#!/bin/bash

tar -czvf BKUP_$(hostname)_$(date +%y.%m.%d).tar /home/pi --exclude="/home/pi/google_drive"
mv        BKUP_$(hostname)_$(date +%y.%m.%d).tar ./google_drive
cd ./google_drive 
#./grive
sudo mount -t nfs casadonfs:/nfs/NFS/Backups /bkups
mv        BKUP_$(hostname)_$(date +%y.%m.%d).tar /bkups
cd ..
