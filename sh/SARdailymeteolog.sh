
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
cd $DBpath
echo "====="$(hostname)"==========" 	>>SARfcst$(date  +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARmetar$(date +%y%m%d).log
echo "==============="        		>>SARmetar$(date +%y%m%d).log
echo $(date +%H:%M:%S)      		>>SARfcst$(date  +%y%m%d).log
echo "==============="        		>>SARfcst$(date  +%y%m%d).log
echo "====="$(hostname)"==========" 	>>SARmetar$(date +%y%m%d).log
python3 ~/src/SARsrc/ogndb/DBmeteo.py 	>>SARmetar$(date +%y%m%d).log
mv metar*.log SARmet* log/
mv fcst*.log  SARfcs* log/
cd 
