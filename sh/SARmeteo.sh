#!/bin/bash
cd /nfs/OGN/DIRdata
echo $(date +%H:%M:%S)                 >>SARmetar$(date +%y%m%d).log
echo "============="                   >>SARmetar$(date +%y%m%d).log
python3 ../src/SARsrc/SARmeteo-lemd.py >>SARmetar$(date +%y%m%d).log
echo "======"$(hostname)"======="      >>SARmetar$(date +%y%m%d).log
cd 
