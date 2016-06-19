#!/bin/bash
cd /nfs/OGN/DIRdata
day=`date "+%a"`
DMY=`date "+%x"`
now=`date "+%R"`
taken=$day"_"$DMY"_"$now

python ../src/processogn.py >>proc$(date +%y%m%d).log
echo $(date +%H:%M:%S)      >>proc$(date +%y%m%d).log
echo "============="        >>proc$(date +%y%m%d).log
python ../src/buildogndb.py prt >>proc$(date +%y%m%d).log
echo $(date +%H:%M:%S)      >>proc$(date +%y%m%d).log
echo "============="        >>proc$(date +%y%m%d).log
sleep 180
/bin/echo '/bin/sh /home/pi/src/pogn.sh' | at -M $(calcelestial -p sun -m set -q Madrid -H civil) + 15 minutes
 
cat proc$(date +%y%m%d).log | /usr/bin/mutt -a "proc"$(date +%y%m%d)".log" -s "OGN daily report "$taken -- acasado@acm.org
mv DATA*  data
dir='fd/Y'$(date +%y)'/M'$(date +%m)
echo "Moving IGC files to: "$dir    >>proc$(date +%y%m%d).log
echo "====================="        >>proc$(date +%y%m%d).log
# create directory if needed, for example at the beginning of the month
if [ ! -d $dir ]
then
    mkdir $dir
fi
mv FD*    $dir
mv proc*.log log
/bin/echo '/bin/sh /home/pi/src/flight_logger.sh' | at -M $(calcelestial -p sun -m rise -q Madrid) + 60 minutes
rm -f tmp/*.IGC
cd 
rm sent

