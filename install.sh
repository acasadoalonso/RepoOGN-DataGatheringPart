#!/bin/bash
echo							        #
echo "===================================" 			#
echo "Installing the SAR system      ...." 			#
echo "===================================" 			#
echo							        #
if [ $# = 0 ]; then						
	sql='NO'
else
	sql=$1
fi
bash commoninstall.sh $sql					#
sudo apt-get -y autoremove
sudo cat /etc/apache2/apache2.conf html.dir 	>>temp.conf	#
sudo echo "ServerName SAR  " >>temp.conf			#
sudo mv temp.conf /etc/apache2/apache2.conf			#
sudo service apache2 restart					#
if [ -d /etc/local/ ]						#
then								#
    sudo mkdir /etc/local					#
fi								#
echo								#
echo "================================================" 	#
echo "Installing the templates needed  ...." 			#
echo "================================================" 	#
echo								#
pwd								#
sudo cp config.template /etc/local/SARconfig.ini		#
cp aliases ~/.bash_aliases					#
crontab <crontab.data						#
crontab -l 							#
echo								#
echo "================================================" 	#
echo "Check the working directories  ...." 			#
echo "================================================" 	#
echo								#
if [ -f SAROGN.db ]						#
then								#
	rm      SAROGN.db					#
fi								#
sqlite3 SAROGN.db            	     < ogndb/DBschema.sql	#
echo "Create the SARogn loginr-path: Type assigned password"	#
mysql_config_editor set --login-path=SARogn --user=ogn --password 
mysql_config_editor print --all					#
echo "CREATE DATABASE OGNDB" | mysql -u root -pogn		#
if [ $sql = 'MySQL' ]			
then	
   mysql --login-path=SARogn --database OGNDB < ogndb/DBschema.sql	#
else
   mysql -u ogn -pogn --database OGNDB < ogndb/DBschema.sql	#

fi
echo								#
cd /tmp
wget acasado.es:60080/files/GLIDERS.sql
mysql -u ogn -pogn  SWIFACE </tmp/GLIDERS.sql
cd /var/www/html/main						#
if [ $sql = 'docker' ]			
then			
   echo "Create DB in docker ogn ..."				#
   echo "========================================================" #
   echo "CREATE DATABASE if not exists OGNDB" | sudo mysql -u ogn -pogn -h MARIADB
   echo "SET GLOBAL log_bin_trust_function_creators = 1; " | sudo mysql -u ogn -pogn -h MARIADB
   sudo mysql -u ogn -pogn -h MARIADB --database OGNDB <ogndb/DBschema.sql 
   sudo mysql -u ogn -pogn -h MARIADB --database OGNDB </tmp/GLIDERS.sql
fi
rm /tmp/GLIDERS.sql
echo " "		
echo								#
echo "================================================" 	#
echo "Installation mysql done ..."				#
echo "================================================" 	#
echo								#
echo								#
echo								#
pwd								#
if [ ! -d ~/src  ]						#
then								#
	mkdir ~/src   						#
	ln -s $(pwd) ~/src/SARsrc				#
fi								#
echo "================================================" 	#
echo " DIR: /src ..."						#
echo "================================================" 	#
ls -la ~/src							#
echo "================================================" 	#
echo " DIR: /src/SARsrc ..."					#
echo "================================================" 	#
ls -la ~/src/SARsrc						#
echo "================================================" 	#
echo " DIR: /src/SARsrc/sh ..."					#
echo "================================================" 	#
ls -la ~/src/SARsrc/sh						#
echo								#
echo								#
echo "================================================" 	#
echo "Installation calcelestial ..."				#
echo "================================================" 	#
echo								#
echo								#
cp sh/calcelestial.sh ~/src					#
if [ ! -f /usr/local/bin/calcelestial ]				#
then								#
	bash ~/src/SARsrc/sh/calcelestial.sh			#
fi								#
calcelestial -h							#
ls  -la ~/src 							#
sudo cp -r ../CGI-BIN/* ../cgi-bin				#
if [ ! -d /nfs  ]						#
then								#
	sudo mkdir /nfs						#
	sudo mkdir /nfs/OGN					#
	sudo mkdir /nfs/OGN/DIRdata				#
	sudo chown ogn:ogn      /nfs/OGN/DIRdata		#
	sudo chmod 777 /nfs/OGN/DIRdata				#
	cd /var/www/public/					#
	mv SAROGN.db /nfs/OGN/DIRdata				#
	sudo chown ogn:ogn      *				#
	sudo chmod 777 *					#
	sudo chown ogn:ogn      */*				#
	sudo chmod 777 */*					#
fi								#
cd /var/www/html						#
if [ ! -d /var/www/html/DIRdata ]				#
then								#
	sudo ln -s /nfs/OGN/DIRdata /var/www/html/		#
fi								#
cd								#
if [ ! -d /usr/local/apache2  ]					#
then								#
	echo							#
	echo							#
	echo "Password for apache2 ..."				#
	echo "================================================" #
	echo							#
	echo							#
	sudo mkdir /usr/local/apache2   			#
	sudo mkdir /usr/local/apache2/passwd			#
	cd /usr/local/apache2/passwd				#
	echo "Type APACHE password for: acasado"		#
	sudo htpasswd -c passwords acasado			#
fi								#
cd								#
echo								#
echo								#
echo "================================================" 	#
echo "Execute the base starting scripts"			#
echo "================================================" 	#
echo								#
echo								#
bash ~/src/SARsrc/sh/SARfcst.sh					#
/bin/echo '/bin/sh ~/src/SARsrc/sh/SARpogn.sh' | at -M $(calcelestial -p sun -m set -q Madrid -H civil) + 15 minutes #
cd								#
if [ -f /nfs/hosts ]
then
      sudo cat /nfs/hosts >> /etc/hosts				#
fi
bash ~/src/SARsrc/sh/SARboot*					#
pgrep -a python3						#
echo								#
echo								#
echo "================================================" 	#
echo "Install goaccess"						#
echo "================================================" 	#
echo								#
echo								#
if [ ! -f /usr/bin/goaccess ]
then
        if [ ! -f /etc/apt/sources.list.d/goaccess.list ]
        then
	   echo "deb http://deb.goaccess.io/ $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/goaccess.list #
	   wget -O - https://deb.goaccess.io/gnugpg.key | sudo apt-key add - #
	   sudo apt-get update					#
        fi
	sudo apt-get install goaccess				#
fi								#
echo								#
echo								#
echo "================================================" 	#
echo "Optional steps ... "					#
echo "================================================" 	#
echo								#
echo								#
touch SARinstallation.done					#
echo " "							#
echo " "							#
echo " "							#
echo " "							#
echo " "							#
echo "========================================================================================================"	#
echo "Installation done ..."											#
echo "Review the configuration file on /etc/local" 								#
echo "Review the configuration mail, ssmtp and .muttrc "							#
echo "Review the configuration of the crontab and the shell scripts on ~/src " 					#
echo "In order to execute the SAR data crawler execute:  bash ~/src/SARboo*.sh " 				#
echo "Check the placement of the RootDocument on APACHE2 ... needs to be /var/www/html	"			#
echo "If running in Windows under Virtual Box, run dos2unix on /var/www/html and ./main and ~/src	"	#
echo "Install phpmyadmin if needed !!!                                                                   "      #
echo "========================================================================================================"	#
echo " "	
echo " "							#
echo " "							#
echo " "							#
echo " "							#
bash
alias
