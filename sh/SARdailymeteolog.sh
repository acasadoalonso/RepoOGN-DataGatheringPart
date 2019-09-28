cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
echo "==============="        		>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARfcst$(date  +%y%m%d).log
echo "==============="        		>>SARfcst$(date  +%y%m%d).log
python3 ../src/SARsrc/ogndb/DBmeteo.py        	>>SARmetar$(date +%y%m%d).log
mv metar*.log SARmet* log/
mv fcst*.log  SARfcs* log/
cd 
