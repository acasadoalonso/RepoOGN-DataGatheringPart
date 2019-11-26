import sqlite3
import config
conn=sqlite3.connect(config.SQLite3)
curs=conn.cursor()
curs.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs.description]
print(("STATIONS-->", colnames)) 
curs.execute('select * from RECEIVERS')
colnames = [desc[0] for desc in curs.description]
print(("RECEIVERS-->", colnames))
curs.execute('select * from OGNDATA')
colnames = [desc[0] for desc in curs.description]
print(("OGNDATA-->", colnames))
curs.execute('select * from GLIDERS')
colnames = [desc[0] for desc in curs.description]
print(("GLIDERS-->", colnames))
curs.execute('select * from METEO')
colnames = [desc[0] for desc in curs.description]
print(("METEO-->", colnames))

conn.commit()
