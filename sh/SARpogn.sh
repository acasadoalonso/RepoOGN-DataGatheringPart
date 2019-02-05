#!/bin/bash
cd /nfs/OGN/DIRdata
day=`date "+%a"`
DMY=`date "+%x"`
now=`date "+%R"`
taken=$day"_"$DMY"_"$now

pnum=$(pgrep python)
if [ $? -eq 0 ] # if OGN repo interface is  not running
then
	sudo kill $pnum
	logger  -t $0 "OGN Repo is alive, should be down"
	echo "Process running: "$pnum >>proc$(date +%y%m%d).log
fi
python ../src/processogn.py 					>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
echo $(date +%H:%M:%S)      					>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
python ../src/buildogndb.py prt 				>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
python ../src/buildogndb.py MYSQL DATA$(date +%y%m%d).log  	>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
echo $(date +%H:%M:%S)      					>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
python ../src/analysisrelay.py -n DATA$(date +%y%m%d).log -i 5	>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
echo $(date +%H:%M:%S)      					>>proc$(date +%y%m%d).log
echo "============="        					>>proc$(date +%y%m%d).log
sleep 180
/bin/echo '/bin/sh ~/src/SARpogn.sh' | at -M $(calcelestial -n -p sun -m set -q Madrid -H civil) + 15 minutes
 
cat proc$(date +%y%m%d).log | /usr/bin/mutt -a "proc"$(date +%y%m%d)".log" -s "OGN daily report "$taken -- angel@acasado.es
mv DATA*  data
rm SAR.alive
rm SAR.sunset
dir='fd/Y'$(date +%y)'/M'$(date +%m)
echo "Moving IGC files to: "$dir    				>>proc$(date +%y%m%d).log
echo "====================="        >>proc$(date +%y%m%d).log
# create directory if needed, for example at the beginning of the month
if [ ! -d $dir ]
then
    mkdir $dir
fi
mv FD*    $dir
mv proc*.log log
/bin/echo '/bin/sh ~/src/SARflight_logger.sh' | at -M $(calcelestial -n -p sun -m rise -q Madrid) + 60 minutes
rm -f tmp/*.IGC
atq 
rm sent

