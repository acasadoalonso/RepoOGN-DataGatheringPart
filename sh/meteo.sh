cd /nfs/OGN/DIRdata
python ../src/lemd.py       >>metar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      >>metar$(date +%y%m%d).log
echo "============="        >>metar$(date +%y%m%d).log
cd 
