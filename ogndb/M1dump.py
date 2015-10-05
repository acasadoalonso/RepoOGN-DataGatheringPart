import sqlite3
print "Meteo on METEO.db"
conn=sqlite3.connect('METEO.db')
curs=conn.cursor()
curs.execute('select * from meteo')
for row in curs.fetchall():
    print row
conn.commit()
conn.close()
