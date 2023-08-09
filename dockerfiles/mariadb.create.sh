#!/bin/bash

echo "Create the MySQL database OGNDB "											#
echo "================================================" 								#
echo "CREATE DATABASE  if not exists OGNDB " | mysql -h mariadb -u root -pogn   					#
mysql -h mariadb -u root -pogn --database OGNDB < DBschema.sql								#
echo "Create the MySQL OGN user "											#
sudo mysql -h mariadb -u root -pogn <../doc/adduser.sql    									#
echo " "														#

