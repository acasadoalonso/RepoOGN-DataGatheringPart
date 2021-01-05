#!/bin/bash 
echo "DROP DATABASE OGNDB if exists" | mysql OGNDB -h 172.17.0.2 -u root -pogn 
echo "CREATE DATABASE OGNDB if not exists" | mysql OGNDB -h 172.17.0.2 -u root -pogn 
mysql OGNDB -h 172.17.0.2 -u root -pogn </tmp/DBschema.sql
