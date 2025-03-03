#!/usr/bin/python3
import sqlite3
import sys
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
conn1=sqlite3.connect(r'SARMETEO.db')
print (config.DBpath+config.SQLite3)
conn2=sqlite3.connect(config.DBpath+config.SQLite3)
curs1=conn1.cursor()
curs2=conn2.cursor()
curs3=conn1.cursor()
# print the dictionaries
curs1.execute('select * from METEO')
colnames = [desc[0] for desc in curs1.description]
print(("METEO1-->", colnames))
curs2.execute('select * from METEO')
colnames = [desc[0] for desc in curs2.description]
print(("METEO2-->", colnames))
# get all the data from METEO.db
curs1.execute('select * from METEO')
curs3.execute('select * from WX')
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

print(("Meteo data", cntm, cntw, " records moved into SAROGN.db")) 
conn1.close()
conn2.close()
