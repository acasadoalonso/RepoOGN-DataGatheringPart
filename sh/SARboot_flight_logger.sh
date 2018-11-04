#!//bin/sh
PATHSRC=/nfs/OGN/src
dir='/nfs/OGN/DIRdata'
# test if directory is available
if [ ! -d $dir ]
then
#       sleep 2 mins for the NFS to start up
	sudo service rpcbind start
	sudo mount casadonfs:/nfs/NFS/Documents /nfs
	sleep 120 
fi
cd $dir
echo "..............." >>getogn.log 
date                   >>getogn.log 
echo "..............." >>err.log 
date                   >>err.log 
python $PATHSRC/SARcalsunrisesunset.py >>getogn.log
python $PATHSRC/ognES.py >>getogn.log  2>>err.log &
cd
