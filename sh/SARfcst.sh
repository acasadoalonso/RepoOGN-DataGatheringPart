cd /nfs/OGN/DIRdata
python ../src/SARsrc/fcst.py >>SARfcst$(date +%y%m%d).log
echo $(date +%H:%M:%S)      >>SARfcst$(date +%y%m%d).log
echo "============="        >>SARfcst$(date +%y%m%d).log
/bin/echo '/bin/sh ~/src/SARsrc/sh/SARfcst.sh' | at -M $(date +%H:%M)+ 6 hours
cd 
