#!/bin/bash
if [ -f ~/.ssh/id_rsa.pub ]
then
	echo "OK"
else
	ssh-keygen
fi
ssh-copy-id -i ~/.ssh/id_rsa.pub $1
echo "Loggin into remote host"
ssh $1


