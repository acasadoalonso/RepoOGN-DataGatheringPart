#!/usr/bin/python3
import sqlite3
import config
print("Meteo on METEO.db")
conn=sqlite3.connect(config.DBpath+'SARMETEO.db')
curs=conn.cursor()
curs.execute('select * from meteo')
for row in curs.fetchall():
    print(row)
conn.commit()
conn.close()
