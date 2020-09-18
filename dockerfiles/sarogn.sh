HOSTIP=`ip -4 addr show scope global dev eth0 | grep inet | awk '{print $2}' | cut -d / -f 1 | sed -n 1p`
docker run  --add-host=docker:${HOSTIP} \
 --add-host=ubuntu:192.168.1.14 \
 --add-host=casadoix2:192.168.1.11 \
 --add-host=casadonas:192.168.1.10 \
 -h testsar \
 -it  \
 --ip="172.17.0.5"  \
 --rm  \
 --link mysql \
 -e CONFIGDIR="/var/www/local/" \
 -e PUBLIC_DIR="public" \
 -p 10019:80/tcp \
 -p 20019:22/tcp \
 --log-opt tag="{{.Name}}/{{.ID}}" \
 --log-driver syslog \
 --log-opt syslog-address=udp://localhost:514 \
 --log-opt syslog-facility=local0 \
 -v /etc/localtime:/etc/localtime:ro \
 -v /var/log/containers/sarogn:/var/log/container:ro \
 -v /etc/local/:/var/www/local/ \
 -v /nfs/OGN/DIRdata:/var/www/data/ \
 -v /nfs/OGN/src:/var/www/src/ \
 -v /etc/sudoers.d:/etc/sudoers.d:ro \
 --name=sarogn \
 acasado/sarogn bash

