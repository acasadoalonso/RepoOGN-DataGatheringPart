#!/bin/bash                                  
                                               
TESTIP=192.168.1.1                           
                                               
ping -c4 ${TESTIP} > /dev/null               
                                               
if [ $? != 0 ]                               
then                                         
    logger -t $0 "WiFi seems down, restarting"
    ifdown --force wlan0                     
    ifup wlan0                               
else                                        
    logger -t $0 "WiFi seems up."           
fi                                               
