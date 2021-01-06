#!/bin/bash
echo "DROP TABLE GLIDERS" | mysql OGNDB -h 172.17.0.2 -u root -pogn 
mysql OGNDB -h 172.17.0.2 -u root -pogn </tmp/GLIDERS.sql
