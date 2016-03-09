#!/bin/sh
rsync -ru /nfs/OGN/DIRdata/ /casadonfs/OGN/DIRdata/
sudo umount /nfs
sudo umount /casadonfs
sudo umount /var/www/ogn
sudo mount -t nfs casadonfs:/nfs/NFS/Documents             /nfs
sudo mount -t nfs casadonfs:/nfs/NFS/Documents/OGN/DIRdata /var/www/ogn
sudo mount -t nfs casadoix2:/Documents                     /casadonfs
df

