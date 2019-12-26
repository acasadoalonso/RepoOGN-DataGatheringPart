#!/bin/bash

if [ ! -d /bkups/OGN ]
then
	sudo mount -t nfs casadonfs:/nfs/NFS/Backups /bkups
fi
if [  -d /bkups/OGN ]
then
	tar -czf /bkups/OGN/BKUP_$(hostname)_$(date +%y.%m.%d).tar ~/ --exclude="~/google_drive" --recursion
fi
cd ..
