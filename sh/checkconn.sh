#!/bin/sh
ip a >tmp.tmp
#echo $1
grep -q $2 tmp.tmp || (sudo ifdown $2 && sudo ifup $2)
rm tmp.tmp
