#!/usr/bin/python3
import sqlite3
import sys
import os
import time
import config
prtreq =  sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False
cntm=0
cntw=0
    
print("Move meteo data from SARMETEO.db to SAROGN.db")
print("=============================================")
#					  report the program version based on file date
print("Program Version:", time.ctime(os.path.getmtime(__file__)))
print("============================================")

print (config.DBpath+config.SQLite3)
conn1=sqlite3.connect(r'SARMETEO.db')
conn2=sqlite3.connect(config.DBpath+config.SQLite3)
curs1=conn1.cursor()			# cursor for SARMETEO(METEO
curs2=conn2.cursor()			# cursor for SAROGN
curs3=conn1.cursor()			# cursor for SARMETEO/WX
# print the dictionaries
curs1.execute('select * from METEO')
colnames = [desc[0] for desc in curs1.description]
print(("METEO1-->", colnames))
curs2.execute('select * from METEO')
colnames = [desc[0] for desc in curs2.description]
print(("METEO2-->", colnames))
curs3.execute('select * from WX')
colnames = [desc[0] for desc in curs3.description]
print(("METEO3-->", colnames))
#
# get all the data from METEO.db
curs1.execute('select * from METEO')
curs3.execute('select * from WX')
# move now the METEO records
while True:
    row=curs1.fetchone()
    if not row: break
    if prt:
        print(row)
    try:					# add the data to SAROGN.db
        curs2.execute("insert into METEO values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]))
        cntm+=1
    except:
        print(("Non unique", row[0],row[1], row[2]))	# ignore the non unique

# move now the WX records
while True:
    row=curs3.fetchone()
    if not row: break
    if prt:
        print(row)
    try:					# add the data to SAROGN.db
        curs2.execute("insert into WX values (?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        cntw+=1
    except:
        print(("Non unique", row[0],row[1], row[2]))	# ignore the non unique

conn2.commit()					# commit the changes
if prt:
    # print the new data
    rows=curs2.execute('select * from METEO')
    rows=curs2.fetchall()
    print(rows)
    # print the new data
    rows=curs2.execute('select * from WX')
    rows=curs2.fetchall()
    print(rows)

# delete the data from METEO.db
curs1.execute('delete from METEO')
curs1.execute('delete from WX')
conn1.commit()					# commit the changes

print(("Meteo data (met & wx) ", cntm, cntw, " records moved into SAROGN.db")) 
conn1.close()
conn2.close()
