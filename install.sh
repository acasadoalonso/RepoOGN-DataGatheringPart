#!/bin/bash
echo								                            #
echo "Installing the SAR system      ...." 			#
echo "===================================" 			#
echo								                            #
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
sudo apt-get install -y software-properties-common python-software-properties #
#sudo rm /etc/apt/sources.list.d/ondre*				#
#sudo add-apt-repository ppa:ondrej/php				#
echo								#
echo " lets update the operating system libraries  ...." 	#
echo								#
sudo apt-get update						#
sudo apt-get install -y language-pack-en-base 			#
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
echo "export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 " >>~/.profile #
echo "export LD_LIBRARY_PATH=/usr/local/lib" >>~/.profile 	#
sudo apt-get -y upgrade					   	#
sudo apt-get -y dist-upgrade					#
cd -								#
echo								#
echo "Installing the packages required . (LAMP stack)..."	#
echo								#
sudo apt-get install -y mysql-server mysql-client sqlite3	#
sudo apt-get install -y python-dev python-pip python-mysqldb    #
sudo apt-get install -y dos2unix libarchive-dev	 autoconf mc	#
sudo apt-get install -y pkg-config git mutt git-core		#
sudo apt-get install -y apache2 php php-mcrypt php-mysql php-cli #
sudo apt-get install -y php-mbstring php-gettext		#
sudo apt-get install -y mailutils ntpdate mutt	ssmtp		#
sudo apt-get install -y libcurl4-openssl-dev			#
sudo apt-get install -y libjson0 libjson0-dev			#
sudo apt-get install -y libnova-0.14-0				#
sudo apt-get install -y libfap 					#
sudo apt-get install -y libfap-dev                              #
sudo apt-get install -y goaccess 				#
sudo apt-get install -y avahi-daemon 				#
sudo a2enmod rewrite						#
sudo a2enmod cgi						#
sudo phpenmod mcrypt						#
sudo phpenmod mbstring						#
sudo a2enmod php7.2 
sudo cat /etc/apache2/apache2.conf html.dir 	>>temp.conf	#
sudo echo "ServerName SAR  " >>temp.conf			#
sudo mv temp.conf /etc/apache2/apache2.conf			#
sudo service apache2 restart					#
echo								#
echo "Installing phpmyadmin  ... "				#
echo								#
sudo apt-get install -y phpmyadmin 				#
sudo service apache2 restart					#
sudo -H pip install --upgrade pip                               #
sudo -H pip install ephem 					#
sudo -H pip install pytz 					#
sudo -H pip install geopy 					#
sudo -H pip install configparser 				#
sudo -H pip install pycountry 					#
sudo -H pip install requests 					#
sudo -H pip install mysql-python				#
if [ ! -d /etc/local ]						#
then								#
    sudo mkdir /etc/local					#
fi								#
echo								#
echo "Installing the templates needed  ...." 			#
echo								#
sudo cp config.template /etc/local/SARconfig.ini		#
sudo cp aliases ~/.bash_aliases					#
if [ -f OGN.db ]						#
then								#
	rm      OGN.db						#
fi								#
sqlite3 OGN.db            < ogndb/DBschema.sql			#
echo "CREATE DATABASE OGNDB" | mysql -u root -pogn		#
mysql -u root -pogn --database OGNDB < ogndb/DBschema.sql	#
echo								#
echo								#
echo "Installation mysql done ..."				#
echo								#
echo								#
cp aliases ~/.bash_aliases					#
crontab <crontab.data						#
crontab -l 							#
if [ ! -d ~/src  ]						#
then								#
	mkdir ~/src   						#
	mkdir ~/src/SARsrc					#
fi								#
cp sh/*.sh ~/src						#
echo								#
echo								#
echo "Installation calcelestial ..."				#
echo								#
echo								#
cp calcelestial.sh ~/src					#
bash ~/src/calcelestial.sh					#
calcelestial -h							#
cp *.py ~/src/SARsrc						#
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
if [ ! -f DIRdata ]						#
then								#
	ln -s /nfs/OGN/DIRdata .				#
fi								#
cd								#
if [ ! -d /usr/local/apache2  ]					#
then								#
	sudo mkdir /usr/local/apache2   			#
	sudo mkdir /usr/local/apache2/passwd			#
	cd /usr/local/apache2/passwd				#
	echo "Type password for: acasado" 			#
	sudo htpasswd -c passwords acasado			#
fi								#
cd								#
echo "Execute the base starting scripts"			#
bash ~/src/fcst.sh						#
/bin/echo '/bin/sh ~/src/SARpogn.sh' | at -M $(calcelestial -p sun -m set -q Madrid -H civil) + 15 minutes #
cd								#
sudo cat /etc/hosts /nfs/hosts > /etc/hosts			#
bash ~/src/SARboot*						#
echo "deb http://deb.goaccess.io/ $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/goaccess.list #
wget -O - https://deb.goaccess.io/gnugpg.key | sudo apt-key add - #
sudo apt-get update						#
sudo apt-get install goaccess					#
echo								#
echo "Optional steps ... "					#
echo								#
sudo dpkg-reconfigure tzdata					#
sudo apt-get -y dist-upgrade					#
sudo apt-get -y autoremove					#
touch SARinstallation.done					#
echo								#
echo "========================================================================================================"	#
echo "Installation done ..."											#
echo "Review the configuration file on /etc/local 								#
echo "Review the configuration mail, ssmtp and .muttrc 								#
echo "Review the configuration of the crontab and the shell scripts on ~/src " 					#
echo "In order to execute the SAR data crawler execute:  bash ~/src/SARboo*.sh " 				#
echo "Check the placement of the RootDocument on APACHE2 ... needs to be /var/www/html				#
echo "If running in Windows under Virtual Box, run dos2unix on /var/www/html and ./main and ~/src		#
echo "Install phpmyadmin if needed !!!                                                                          #
echo "========================================================================================================"	#
echo								#
