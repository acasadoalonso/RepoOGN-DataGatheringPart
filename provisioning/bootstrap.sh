#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y apache2
sudo -u vagrant ln -s /vagrant/public/main ~/src
if [ -f /nfs/hosts ]
then 
	sudo cat /nfs/hosts >>/etc/hosts
fi

if [ -f /tmp/commoninstall.sh ]
then 
        sudo bash /tmp/commoninstall.sh
	echo "Install the rest of the software running     bash /tmp/commoninstall.sh"
	echo "follow by running                            bash /tmp/install.sh"
fi
sudo apt-get autoremove
