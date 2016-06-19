#!/bin/sh
sudo service rpcbind start
sudo mount -t nfs casadonfs:/nfs/NFS/Documents             /nfs
sudo mount -t nfs casadonfs:/nfs/NFS/Documents/OGN/DIRdata /var/www/ogn
sudo mount -t nfs casadoix2:/Documents                     /oldnfs
df

