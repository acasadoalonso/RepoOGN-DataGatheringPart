#!/usr/bin/python3
import sqlite3
path="/nfs/OGN/DIRdata/"
print("Meteo on METEO.db")
conn=sqlite3.connect(path+'METEO.db')
curs=conn.cursor()
curs.execute('select * from meteo')
for row in curs.fetchall():
    print(row)
conn.commit()
conn.close()
