#!//bin/sh
cd /nfs/OGN/DIRdata
echo "..............." >>SARgetogn.log 
date                   >>SARgetogn.log 
calcelestial -p sun -m set -q Madrid -H civil >>SARgetogn.log 
echo "..............." >>SARerr.log 
date                   >>SARerr.log 
calcelestial -p sun -m set -q Madrid -H civil >>SARerr.log 
echo "..............." >>SARerr.log 
python3 ../src/SARsrc/SARcalsunrisesunset.py >>SARgetogn.log
python3 ../src/SARsrc/ognES.py               >>SARgetogn.log  2>>SARerr.log &
cd
