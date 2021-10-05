#!/bin/bash
if [ ! -f /tmp/.DBpasswd    ]
then
   echo "Type DB password ..."
   read DBpasswd
   echo $DBpasswd > /tmp/.DBpasswd
fi
mysql -h 172.17.0.2 -u root -p$(cat /tmp/.DBpasswd) </tmp/adduser.sql
