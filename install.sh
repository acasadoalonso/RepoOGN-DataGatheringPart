#!/bin/bash
echo							        #
echo "Installing the SAR system      ...." 			#
echo "===================================" 			#
echo							        #
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
sudo apt-get install -y software-properties-common python3-software-properties #
#sudo rm /etc/apt/sources.list.d/ondre*				#
#sudo add-apt-repository ppa:ondrej/php				#
echo								#
echo "Lets update the operating system libraries  ...." 	#
echo "================================================" 	#
echo								#
sudo apt-get update						#
sudo apt-get install -y language-pack-en-base 			#
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
echo "export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 " >>~/.profile #
echo "export LD_LIBRARY_PATH=/usr/local/lib" >>~/.profile 	#
sudo apt-get -y upgrade					   	#
sudo apt-get -y dist-upgrade					#
echo								#
echo "Installing the packages required . (LAMP stack)..."	#
echo "==================================================" 	#
echo								#
sudo apt-get install -y mysql-server mysql-client sqlite3	#
sudo apt-get install -y python3-dev python3-pip python3-mysqldb #
sudo apt-get install -y dos2unix libarchive-dev	 autoconf mc	#
sudo apt-get install -y pkg-config git mutt git-core		#
sudo apt-get install -y apache2 php php-mcrypt php-mysql php-cli #
sudo apt-get install -y php-mbstring php-gettext		#
sudo apt-get install -y mailutils ntpdate mutt	ssmtp		#
sudo apt-get install -y libcurl4-openssl-dev			#
sudo apt-get install -y libjson0 libjson0-dev			#
sudo apt-get install -y libjson-c-dev 				#
sudo apt-get install -y libnova-0.14-0				#
sudo apt-get install -y libfap-dev                              #
sudo apt-get install -y at	 				#
sudo apt-get install -y avahi-daemon 				#
sudo apt-get install -y php7.2	 				#
sudo a2enmod rewrite						#
sudo a2enmod cgi						#
sudo phpenmod mcrypt						#
sudo phpenmod mbstring						#
sudo a2enmod php7.2 						#
sudo cat /etc/apache2/apache2.conf html.dir 	>>temp.conf	#
sudo echo "ServerName SAR  " >>temp.conf			#
sudo mv temp.conf /etc/apache2/apache2.conf			#
sudo service apache2 restart					#
echo								#
echo "Installing phpmyadmin  ... "				#
echo "================================================" 	#
echo								#
sudo apt-get install -y libmysqlclient-dev			#
sudo apt-get install -y phpmyadmin 				#
sudo service apache2 restart					#
echo								#
echo "Installing python modules  ... "				#
echo "================================================" 	#
echo								#
sudo -H pip3 install --upgrade pip                              #
sudo -H pip3 install --upgrade setuptools			#
sudo -H pip3 install ephem 					#
sudo -H pip3 install pytz 					#
sudo -H pip3 install geopy 					#
sudo -H pip3 install configparser 				#
sudo -H pip3 install pycountry 					#
sudo -H pip3 install requests 					#
sudo -H pip3 install MySQL-python				#
sudo -H pip3 install beeprint					#
sudo -H pip3 install ogn.client					#
if [ ! -d /etc/local ]						#
then								#
    sudo mkdir /etc/local					#
fi								#
echo								#
echo "Installing the templates needed  ...." 			#
echo "================================================" 	#
echo								#
pwd								#
sudo cp config.template /etc/local/SARconfig.ini		#
cp aliases ~/.bash_aliases					#
crontab <crontab.data						#
crontab -l 							#
echo								#
echo "Check the working directories  ...." 			#
echo "================================================" 	#
echo								#
if [ -f OGN.db ]						#
then								#
	rm      OGN.db						#
fi								#
sqlite3 OGN.db            	     < ogndb/DBschema.sql	#
echo "CREATE DATABASE OGNDB" | mysql -u root -pogn		#
mysql -u root -pogn --database OGNDB < ogndb/DBschema.sql	#
echo								#
echo								#
echo "Installation mysql done ..."				#
echo "================================================" 	#
echo								#
echo								#
echo
pwd
if [ ! -d ~/src  ]						#
then								#
	mkdir ~/src   						#
	ln -s $(pwd) ~/src/SARsrc				#
fi								#
ls -la ~/src							#
ls -la ~/src/SARsrc						#
ls -la ~/src/SARsrc/sh						#
echo								#
echo								#
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
	mv OGN.db /nfs/OGN/DIRdata				#
	sudo chown ogn:ogn      *				#
	sudo chmod 777 *					#
	sudo chown ogn:ogn      */*				#
	sudo chmod 777 */*					#
fi								#
cd /var/www/html						#
if [ ! -f /var/www/html/DIRdata ]						#
then								#
	sudo ln -s /nfs/OGN/DIRdata .				#
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
echo "Execute the base starting scripts"			#
echo "================================================" 	#
echo								#
echo								#
bash ~/src/SARsrc/sh/SARfcst.sh						#
/bin/echo '/bin/sh ~/src/SARsrc/sh/SARpogn.sh' | at -M $(calcelestial -p sun -m set -q Madrid -H civil) + 15 minutes #
cd								#
sudo cat /etc/hosts /nfs/hosts > /etc/hosts			#
bash ~/src/SARsrc/sh/SARboot*						#
pgrep -a python3						#
echo								#
echo								#
echo "Install goaccess"						#
echo "================================================" 	#
echo								#
echo								#
if [ ! -f /usr/bin/goaccess ]
then
	echo "deb http://deb.goaccess.io/ $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/goaccess.list #
	wget -O - https://deb.goaccess.io/gnugpg.key | sudo apt-key add - #
	sudo apt-get update					#
	sudo apt-get install goaccess				#
fi								#
echo								#
echo								#
echo "Optional steps ... "					#
echo "================================================" 	#
echo								#
echo								#
sudo dpkg-reconfigure tzdata					#
sudo apt-get -y dist-upgrade					#
sudo apt-get -y autoremove					#
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
