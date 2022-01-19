#!/bin/bash
sudo service docker stop
sudo cp daemon.json /etc/docker/
sudo rsync -aP /var/lib/docker/ /wrk/docker/
sudo mv /var/lib/docker /var/lib/docker.old
sudo service docker start
