ulimit -Hn
ulimit -Sn
id
sysctl -w fs.file-max=100000
vi /etc/sysctl.conf
    add fs.file-max = 100000
sysctl -p
cat /proc/sys/fs/file-max

