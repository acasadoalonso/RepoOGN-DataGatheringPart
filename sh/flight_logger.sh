#!//bin/sh
cd /nfs/OGN/DIRdata
echo "..............." >>getogn.log 
date                   >>getogn.log 
calcelestial -p sun -m set -q Madrid -H civil >>getogn.log 
echo "..............." >>err.log 
date                   >>err.log 
calcelestial -p sun -m set -q Madrid -H civil >>err.log 
echo "..............." >>err.log 
python ../src/ognES.py >>getogn.log  2>>err.log &
cd
