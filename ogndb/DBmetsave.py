import sqlite3
print "Save METEO data from OGN on METEO DB"
print "===================================="
conn2=sqlite3.connect(r'METEO.db')
conn1=sqlite3.connect(r'OGN.db')
curs1=conn1.cursor()
curs2=conn2.cursor()
#create the table 
crecmd="create table IF NOT EXISTS METEO (date char(6), time char (6), metstation char(4), rowdata TEXT NULL DEFAULT NULL, temp REAL, dewp REAL, winddir int, windspeed int, windgust int, visibility int, qnh REAL, cloud TEXT, fcat TEXT, wxstring TEXT)"
curs2.execute(crecmd)
crecmd="create unique index IF NOT EXISTS METEOIDX on METEO ( date , time)"
curs2.execute(crecmd)
# print the dictionaries
curs1.execute('select * from METEO')
colnames = [desc[0] for desc in curs1.description]
print "METEO1-->", colnames
curs2.execute('select * from METEO')
colnames = [desc[0] for desc in curs2.description]
print "METEO2-->", colnames
# retrieve all the data from OGN and save it on METEO
curs1.execute('select * from METEO')
while True:
    row=curs1.fetchone()
    if not row: break
    print row
    try:
        curs2.execute("insert into METEO values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]))
    except:
        print "Non unique", row[0],row[1]

conn2.commit()
# print the new data base
rows=curs2.execute('select * from METEO')
rows=curs2.fetchall()
print rows
# delete the data on the OGN database
curs1.execute('delete from METEO')
conn1.commit()
conn1.close()
conn2.close()
