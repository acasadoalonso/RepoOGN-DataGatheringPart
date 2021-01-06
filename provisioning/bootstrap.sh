#!/usr/bin/env bash

apt-get update
apt-get install -y apache2
if [ -f /nfs/hosts ]
then 
	sudo cat /nfs/hosts >>/etc/hosts
fi

if [ -f /tmp/commoninstall.sh ]
then 
	echo "Install the rest of the software running     bash /tmp/commoninstall.sh"
	echo "follow by running                            bash /tmp/install.sh"
fi

