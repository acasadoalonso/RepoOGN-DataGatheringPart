#!/usr/bin/python
#
import sqlite3
#-----------------------------------------------------------------

conn=sqlite3.connect(r'OGN.db')			# connect now with the created database
curs=conn.cursor()

print "Print dictionaries:"             
curs.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs.description]
print "STATATIONS", colnames 
curs.execute('select * from RECEIVERS')
colnames = [desc[0] for desc in curs.description]
print "RECEIVERS", colnames
curs.execute('select * from OGNDATA')
colnames = [desc[0] for desc in curs.description]
print "OGNDATA", colnames
curs.execute('select * from GLIDERS')
colnames = [desc[0] for desc in curs.description]
print "GLIDERS", colnames
curs.execute('select * from METEO')
colnames = [desc[0] for desc in curs.description]
print "METEO", colnames
curs.execute('select * from STASTA')
colnames = [desc[0] for desc in curs.description]
print "STASTA", colnames
curs.execute('select * from OGNDATAREG')
colnames = [desc[0] for desc in curs.description]
print "OGNDATAREG", colnames
conn.commit()
conn.close()

