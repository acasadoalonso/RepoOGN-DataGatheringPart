hn=$(hostname)
echo $hn
if [ $hn = 'SAROGN' ]
then
	server="ubuntu"
	server2="casadonfs"
else
	server="localhost"
	server2="localhost"
fi
echo $server $server2
