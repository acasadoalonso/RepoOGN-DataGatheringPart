#!/bin/bash
#
# install SAR interface on a docker container
#
bash install.portainer
make
if [ ! -f .DBpasswd    ]					#
then								#
   echo "Type DB password ..."					#
   read DBpasswd						#
   echo $DBpasswd > .DBpasswd					#
fi	
bash mariadbnet.sh
bash mariadbpma.pull
bash mariadbpma.sh
bash mariadb.sh
docker ps -a
