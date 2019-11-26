#!//bin/sh
cd /nfs/OGN/DIRdata
echo "......"$(hostname)"........." 		>>SARgetogn.log 
date                   				>>SARgetogn.log 
calcelestial -p sun -m set -q Madrid -H civil 	>>SARgetogn.log 
echo "......"$(hostname)"........." 		>>SARerr.log 
date                   				>>SARerr.log 
calcelestial -p sun -m set -q Madrid -H civil 	>>SARerr.log 
echo "......"$(hostname)"........." 		>>SARerr.log 
python3 ../src/SARsrc/SARcalsunrisesunset.py 	>>SARgetogn.log
python3 ../src/SARsrc/SARognES.py             	>>SARgetogn.log  2>>SARerr.log &
cd
