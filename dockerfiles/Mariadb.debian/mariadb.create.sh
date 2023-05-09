#!/bin/bash

echo "Create the MySQL database OGNDB "											#
echo "================================================" 								#
echo "CREATE DATABASE  if not exists OGNDB " | mysql -h mariadb -u root 	   					#
mysql -h mariadb -u root  --database OGNDB 	<../DBschema.sql							#
echo "Create the MySQL OGN user "											#
sudo mysql -h mariadb -u root 			<../adduser.sql    							#
echo "CREATE DATABASE  if not exists PMADB " | mysql -h mariadb -u root 	   					#
echo " "														#

