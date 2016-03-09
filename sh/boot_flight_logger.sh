#!//bin/sh
dir='/nfs/OGN/DIRdata'
# test if directory is available
if [ ! -d $dir ]
then
#       sleep 5 mins for the NFS to start up
	sleep 300 
fi
cd $dir
echo "..............." >>getogn.log 
date                   >>getogn.log 
echo "..............." >>err.log 
date                   >>err.log 
python ../src/ognES.py >>getogn.log  2>>err.log &
cd
