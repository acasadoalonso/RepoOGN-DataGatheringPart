#!/bin/bash

if [ ! -f /tmp/.DBpasswd    ]
then
   echo "Type DB password ..."
   read DBpasswd
   echo $DBpasswd > /tmp/.DBpasswd
fi
echo "DROP TABLE GLIDERS" | mysql OGNDB -h 172.17.0.2 -u root -p$(cat /tmp/.DBpasswd) 
mysql OGNDB -h 172.17.0.2 -u root -p$(cat /tmp/.DBpasswd) </tmp/GLIDERS.sql
