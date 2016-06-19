#!/bin/bash
ss=$(calcelestial -p sun -m set -q Madrid -f %s)
now=$(date +%s)
echo $ss
echo $now
let "dif=$ss-$now"
echo $dif
if [ $dif -lt 0 ]
then echo Nothin to do
else echo check
fi
