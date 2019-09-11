#!//bin/sh
dir='/nfs/OGN/DIRdata'
# test if directory is available
if [ ! -d $dir ]
then
#       sleep 2 mins for the NFS to start up
	#sudo service rpcbind start
	sudo mount casadonfs:/nfs/NFS/Documents /nfs
	sleep 120 
fi
cd $dir
echo "..............." >>SARgetogn.log 
date                   >>SARgetogn.log 
echo "..............." >>SARerr.log 
date                   >>SARerr.log 
python3 ../src/SARsrc/SARcalsunrisesunset.py >>SARgetogn.log
python3 ../src/SARsrc/ognES.py               >>SARgetogn.log  2>>SARerr.log &
cd
