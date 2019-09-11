cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      >>SARmetar$(date +%y%m%d).log
echo "============="        >>SARmetar$(date +%y%m%d).log
python ../src/SARsrc/lemd.py >>SARmetar$(date +%y%m%d).log
echo "============="        >>SARmetar$(date +%y%m%d).log
cd 
