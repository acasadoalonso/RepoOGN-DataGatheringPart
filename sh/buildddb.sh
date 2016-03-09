cd /nfs/OGN/src/flarmdb
rm *.fln
rm *.csv
wget -o flarmdata.log  www.flarmnet.org/files/data.fln
mv data.fln flarmdata.fln
wget -o ognddbdata.log ddb.glidernet.org/download
mv download ognddbdata.csv
python ognbuildfile.py 
python flarmbuildfile.py 
cat flarmhdr flarmdata.txt  >flarmdata.py 
cat ognhdr   ognddbdata.txt >ognddbdata.py 
cat kglidhdr ognddbdata.py  flarmdata.py kglidtrail >kglid.py
rm ../kglid.bkup
mv ../kglid.py kglid.bkup
cp kglid.py ../
ls -la
cd 
