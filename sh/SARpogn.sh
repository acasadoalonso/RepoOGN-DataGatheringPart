#!/bin/bash
if [ $# = 0 ]; then
	city='Madrid'
else
	city=$1
fi

if [ -z $CONFIGDIR ]
then 
     export CONFIGDIR=/etc/local/
fi
DBpath=$(echo    `grep '^DBpath '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpath //g' | sed 's/ //g' )
DBuser=$(echo    `grep '^DBuser '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBuser //g' | sed 's/ //g' )
DBpasswd=$(echo  `grep '^DBpasswd ' $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBpasswd //g' | sed 's/ //g' )
server=$(echo    `grep '^DBhost '   $CONFIGDIR/SARconfig.ini` | sed 's/=//g' | sed 's/^DBhost //g' | sed 's/ //g' )
cd $DBpath
day=`date "+%a"`
DMY=`date "+%x"`
now=`date "+%R"`
taken=$day"_"$DMY"_"$now
dt=$(date +%y%m%d)
echo "Server: "$(hostname)" DBhost: "$server			>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
pnum=$(pgrep python3)
if [ $? -eq 0 ] # if OGN repo interface is  not running
then
	sudo kill $pnum
	logger  -t $0 "OGN Repo is alive, should be down at sunset "$(hostname)
	echo $(hostname)" Process running at sunset: "$pnum 	>>SARproc$dt.log
fi
# gen the IGC files
python3 ~/src/SARsrc/SARprocessogn.py 				>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
# Store the records on the sqlite3 DDBB
python3 ~/src/SARsrc/SARbuildogndb.py prt			>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
# Store the records now  on the MYSQL DDBB as well
python3 ~/src/SARsrc/SARbuildogndb.py MYSQL DATA$dt.log  	>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
python3 ~/src/SARsrc/SARanalysisrelay.py -n DATA$dt.log -i 5 -sa YES	>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
sleep 180
/bin/echo '/bin/bash ~/src/SARsrc/sh/SARpogn.sh '$city | at -M $(calcelestial -n -p sun -m set -q $city -H civil) + 15 minutes
# keep a copy for further sync with other servers
mysqldump -u $DBuser -p$DBpasswd -h $server --add-drop-table OGNDB OGNDATA   >$DBpath/files/OGNDATA.sql  2>>SARproc$dt.log 
# send a mail
cat SARproc$(date +%y%m%d).log | /usr/bin/mutt -a "SARproc"$dt".log" -s $(hostname)" OGN daily report "$taken -- $(cat ~/src/SARsrc/sh/mailnames.txt)
mv DATA*  data
rm SAR.alive
rm SAR.sunset
# fddir : directory where to staore the IGC files
fddir='fd/Y'$(date +%y)'/M'$(date +%m)
echo "Moving IGC files to: "$fddir    				>>SARproc$dt.log
echo "====================="        				>>SARproc$dt.log
# create directory if needed, for example at the beginning of the month
if [ ! -d $fddir ]
then
    mkdir -p $fddir
fi
mv FD*    $fddir
echo "Server: "$(hostname)     					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
mv SARproc*.log log
/bin/echo '/bin/bash ~/src/SARsrc/sh/SARflight_logger.sh '$city | at -M $(calcelestial -n -p sun -m rise -q $city) + 60 minutes
rm -f tmp/*.IGC
atq 
rm ~/sent

