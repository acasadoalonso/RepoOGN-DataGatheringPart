#!/bin/bash 
echo "DROP DATABASE IF EXISTS OGNDB "       | mysql  -h 172.17.0.2 -u root -pogn 
echo "CREATE DATABASE IF NOT EXISTS OGNDB " | mysql  -h 172.17.0.2 -u root -pogn 
mysql OGNDB -h 172.17.0.2 -u root -pogn </tmp/DBschema.sql
