ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub $1
ssh $1

