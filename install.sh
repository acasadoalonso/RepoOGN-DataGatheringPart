#!/bin/bash
echo								                            #
echo "Installing the SAR system      ...." 			#
echo "===================================" 			#
echo								                            #
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
sudo apt-get install -y software-properties-common python-software-properties #
sudo rm /etc/apt/sources.list.d/ondre*				#
sudo add-apt-repository ppa:ondrej/php				#
echo								#
echo " lets update the operating system libraries  ...." 	#
echo								#
sudo apt-get update						#
sudo apt-get install -y language-pack-en-base 			#
export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8		#
echo "export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 " >>~/.profile #
echo "export LD_LIBRARY_PATH=/usr/local/lib" >>~/.profile 	#
sudo apt-get -y upgrade					   	#
cd libfap-1.5/deb				             	#
sudo dpkg -i lib*amd64.deb					#
cd -								#
echo								#
echo "Installing the packages required . (LAMP stack)..."	#
echo								#
sudo apt-get install -y mysql-server mysql-client sqlite3	#
sudo apt-get install -y python-dev python-pip python-mysqldb    #
sudo apt-get install -y dos2unix libarchive-dev	 autoconf mc	#
sudo apt-get install -y pkg-config git mutt			#
sudo apt-get install -y apache2 php php-mcrypt php-mysql php-cli #
sudo apt-get install -y php-mbstring php-gettext		#
sudo apt-get install -y mailutils ntpdate mutt	ssmtp		#
sudo a2enmod rewrite						#
sudo a2enmod cgi						#
sudo phpenmod mcrypt						#
sudo phpenmod mbstring						#
sudo cat /etc/apache2/apache2.conf html.dir 	>>temp.conf	#
sudo echo "ServerName SAR  " >>temp.conf			#
sudo mv temp.conf /etc/apache2/apache2.conf			#
sudo service apache2 restart					#
echo								#
echo "Installing phpmyadmin  ... "				#
echo								#
#sudo apt-get install -y phpmyadmin 				#
sudo service apache2 restart					#
sudo -H pip install --upgrade pip                               #
sudo -H pip install ephem 					#
sudo -H pip install pytz 					#
sudo -H pip install geopy 					#
sudo -H pip install configparser 				#
sudo -H pip install pycountry 					#
if [ ! -d /etc/local ]						#
then								#
    sudo mkdir /etc/local					#
fi								#
echo								#
echo "Installing the templates needed  ...." 			#
echo								#
sudo cp config.template /etc/local/SARconfig.ini		#
if [ -f OGN.db ]						#
then								#
	rm      OGN.db						#
fi								#
sqlite3 OGN.db            < ogndb/DBschema.sql			#
echo "CREATE DATABASE OGNDB" | mysql -u root -pogn		#
mysql -u root -pogn --database OGNDB < ogndb/DBschema.sql	#
cp aliases ~/.bash_aliases					#
crontab <crontab.data						#
crontab -l 							#
if [ ! -d ~/src  ]						#
then								#
	mkdir ~/src   						#
	mkdir ~/src/SARsrc					#
fi								#
cp sh/*.sh ~/src						#
cp *.py ~/src/SARsrc						#
ls  -la ~/src 							#
cp -r ../CGI-BIN/* ../cgi-bin					#
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
	ln -s /nfs/OGN/DIRdata .				#
fi								#
cd								#
if [ ! -d /usr/local/apache2  ]					#
then								#
	mkdir /usr/local/apache2   				#
	mkdir /usr/local/apache2/passwd				#
	htpasswd -c passwords acasado				#
fi								#
cd								#
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
echo "Review the configuration of the crontab and the shell scripts on ~/src " 					#
echo "In order to execute the SAR data crawler execute:  bash ~/src/SARlive.sh " 				#
echo "Check the placement of the RootDocument on APACHE2 ... needs to be /var/www/html				#
echo "If running in Windows under Virtual Box, run dos2unix on /var/www/html & ./main & ~/src			#
echo "Install phpmyadmin if needed !!!                                                                          #
echo "========================================================================================================"	#
echo								#
