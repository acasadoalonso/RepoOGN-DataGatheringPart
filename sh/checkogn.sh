#!/bin/bash
p1=$(pgrep -x ./ogn-rf /home/ogn/rtlsdr-ogn.conf)
if [$? -eq 0]
then 
	logger -t $0 "OGN is running"
else
	p2=$(pgrep -x /bin/bash /etc/init.d/rtlsdr-ogn start)
	if [$? -eq 0]
	then 
		exit
	else
		sudo ntpdate -u pool.ntp.org
		sudo service rtlsdr-ogn restart
		logger -t $0 "OGN is restarting"
	fi
fi





