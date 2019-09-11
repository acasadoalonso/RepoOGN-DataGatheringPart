#!/bin/bash
cd /nfs/OGN/DIRdata
day=`date "+%a"`
DMY=`date "+%x"`
now=`date "+%R"`
taken=$day"_"$DMY"_"$now
dt=$(date +%y%m%d)
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
pnum=$(pgrep python)
if [ $? -eq 0 ] # if OGN repo interface is  not running
then
	sudo kill $pnum
	logger  -t $0 "OGN Repo is alive, should be down"
	echo "Process running: "$pnum 				>>SARproc$dt.log
fi
python ../src/SARsrc/processogn.py 				>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
python ../src/SARsrc/buildogndb.py prt 				>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
python ../src/SARsrc/buildogndb.py MYSQL DATA$dt.log  		>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
python ../src/SARsrc/analysisrelay.py -n DATA$dt.log -i 5	>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
echo $(date +%H:%M:%S)      					>>SARproc$dt.log
echo "============="        					>>SARproc$dt.log
sleep 180
/bin/echo '/bin/sh ~/src/SARsrc/sh/SARpogn.sh' | at -M $(calcelestial -n -p sun -m set -q Madrid -H civil) + 15 minutes
 
cat SARproc$(date +%y%m%d).log | /usr/bin/mutt -a "SARproc"$dt".log" -s "OGN daily report "$taken -- angel@acasado.es
mv DATA*  data
rm SAR.alive
rm SAR.sunset
dir='fd/Y'$(date +%y)'/M'$(date +%m)
echo "Moving IGC files to: "$dir    				>>SARproc$dt.log
echo "====================="        				>>SARproc$dt.log
# create directory if needed, for example at the beginning of the month
if [ ! -d $dir ]
then
    mkdir $dir
fi
mv FD*    $dir
mv SARproc*.log log
/bin/echo '/bin/sh ~/src/SARsrc/sh/SARflight_logger.sh' | at -M $(calcelestial -n -p sun -m rise -q Madrid) + 60 minutes
rm -f tmp/*.IGC
atq 
rm sent

