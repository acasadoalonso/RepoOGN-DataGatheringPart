#!/bin/bash
echo "Backup SAROGN files ..."
if [ ! -d /bkups/OGN ]
then
	sudo mount -t nfs casadonewnfs:/nfs/BKUP /bkups
fi
if [  -d /bkups/OGN ]
then
	tar -czf   /bkups/OGN/BKUP_$(hostname)_$(date +%y.%m.%d).tar ~/ 
	sudo umount /bkups
fi
cd ..
