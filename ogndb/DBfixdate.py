import sqlite3
print "Fix the date  from STATIONS OGN DB"
print "=================================="
conn1=sqlite3.connect(r'OGN.db')
curs1=conn1.cursor()
# print the dictionaries
curs1.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs1.description]
print "STATIONS-->", colnames
curs1.execute('select * from OGNDATA')
colnames = [desc[0] for desc in curs1.description]
print "OGNDATA-->", colnames

d=23
m=5
while m <= 9:
	d=1
	while d <=31:
		dt1=("%02d%02d15" % (d, m))
		dt2=("15%02d%02d" % (m, d))
		print dt1, dt2
    		try:
        		curs1.execute("update STATIONS set date=? where date=?", [dt2, dt1])
			print curs1.rowcount
        		curs1.execute("update OGNDATA  set date=? where date=?", [dt2, dt1])
			print curs1.rowcount
    		except:
        		print "Error:", dt1, dt2
		d+=1
	m+=1

conn1.commit()
conn1.close()
