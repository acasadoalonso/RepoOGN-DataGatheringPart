#!/bin/sh
cd calcelestial
rm -r calcelestial
git clone https://github.com/stv0g/calcelestial
cd calcelestial/
sudo apt-get install -y at libnova-dev libcurl4-openssl-dev libjson-c-dev libdb-dev autoconf make gcc pkg-config
#sh autogen.sh
autoreconf -i
./configure
make
sudo make install
cd ..

