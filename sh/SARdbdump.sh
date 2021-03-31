cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "============="        		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "====="$(hostname)"========"	>>log/SARdbdump$(date +%y%m%d-%H).log
python3 ~/src/SARsrc/ogndb/DBdump.py LNAMES 	>>log/SARdbdump$(date +%y%m%d-%H).log
echo $(date +%H:%M:%S)      		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "============="        		>>log/SARdbdump$(date +%y%m%d-%H).log
echo "====="$(hostname)"========"	>>log/SARdbdump$(date +%y%m%d-%H).log
cd 
