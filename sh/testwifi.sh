#!/bin/sh
ip a >tmp.tmp
#echo $1
grep -q $1 tmp.tmp 
if [ $? != 0 ]
then
    logger -t $0 "WiFi seems down, restarting"
    sudo ifdown --force $2
    sudo ifup $2
else
    logger -t $0 "WiFi seems up."
fi
rm tmp.tmp
