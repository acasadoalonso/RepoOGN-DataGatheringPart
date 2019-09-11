#!/bin/bash

if [ ! -d /bkups ]
then
	sudo mount -t nfs casadonfs:/nfs/NFS/Backups /bkups
fi
if [  -d /bkups ]
then
	tar -czvf /bkups/OGN/BKUP_$(hostname)_$(date +%y.%m.%d).tar ~/ --exclude="~/google_drive" --recursion
fi
cd ..
