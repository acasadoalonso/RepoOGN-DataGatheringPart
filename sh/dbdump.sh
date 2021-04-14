
if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
cd $DBpath
echo $(date +%H:%M:%S)      		>>dbdump$(date +%y%m%d-%H).log
echo "============="        		>>dbdump$(date +%y%m%d-%H).log
python3 ~/src/SARsrc/ogndb/DBdump.py LNAMES 	>>dbdump$(date +%y%m%d-%H).log
echo $(date +%H:%M:%S)      		>>dbdump$(date +%y%m%d-%H).log
echo "============="        		>>dbdump$(date +%y%m%d-%H).log
cd 
