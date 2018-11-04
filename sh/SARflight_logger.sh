#!//bin/sh
PATHSRC=/nfs/OGN/src
cd /nfs/OGN/DIRdata
echo "..............." >>getogn.log 
date                   >>getogn.log 
calcelestial -p sun -m set -q Madrid -H civil >>getogn.log 
echo "..............." >>err.log 
date                   >>err.log 
calcelestial -p sun -m set -q Madrid -H civil >>err.log 
echo "..............." >>err.log 
python $PATHSRC/SARcalsunrisesunset.py >>getogn.log
python $PATHSRC/ognES.py >>getogn.log  2>>err.log &
cd
