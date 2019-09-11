#!/usr/bin/python3
import sqlite3
import sys
prtreq =  sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False
cnt=0
    
print("Move meteo data from METEO.db to OGN.db")
print("=======================================")
conn1=sqlite3.connect(r'METEO.db')
conn2=sqlite3.connect(r'OGN.db')
curs1=conn1.cursor()
curs2=conn2.cursor()
# print the dictionaries
curs1.execute('select * from METEO')
colnames = [desc[0] for desc in curs1.description]
print(("METEO1-->", colnames))
curs2.execute('select * from METEO')
colnames = [desc[0] for desc in curs2.description]
print(("METEO2-->", colnames))
# get all the data from METEO.db
curs1.execute('select * from METEO')
while True:
    row=curs1.fetchone()
    if not row: break
    if prt:
        print(row)
    try:					# add the data to OGN.db
        curs2.execute("insert into METEO values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]))
        cnt+=1
    except:
        print(("Non unique", row[0],row[1], row[2]))	# ignore the non unique

conn2.commit()					# commit the changes
if prt:
    # print the new data
    rows=curs2.execute('select * from METEO')
    rows=curs2.fetchall()
    print(rows)
# delete the data from METEO.db
curs1.execute('delete from METEO')
conn1.commit()					# commit the changes
print(("Meteo data", cnt, " records moved into OGN.db")) 
conn1.close()
conn2.close()
