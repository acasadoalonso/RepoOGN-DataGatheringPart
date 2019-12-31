#!/usr/bin/python3
import sqlite3
import config
print("Meteo on SAROGN.db")
conn=sqlite3.connect(config.DBpath+config.SQLite3)
curs=conn.cursor()
curs.execute('select * from meteo')
for row in curs.fetchall():
    print(row)
conn.commit()
conn.close()
