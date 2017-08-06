#!/bin/sh
pgrep noip2
if [ $? -ne 0 ] # if noip2 is  not running
then
 # restart noip2
    logger -t $0 "noip2 seems down, restarting"
    sudo /usr/local/bin/noip2
    logger -t $0 $(pgrep noip2) 
else
    logger -t $0 "nopi2 seems up."
fi
