#!/usr/bin/python
#
import sqlite3
def opendb (schema_file, cursor):
    # Open a connection to the database
    # Build the database from the supplied schema
    print "opendb"
    try:
        db = sqlite3.connect("OGN.db")
    except Exception as e:
        # Failed to open flogger.db, error
        print "Failed to open OGN.db, error"
        return False

    # Create a cursor to work with
    cur = db.cursor()
    cursor[0] = cur

    # Drop tables if they exist in the database
    floggerSchema = open(schema_file)
    print "opendb:", schema_file, " open ok"
    schemaStr = ""
    for line in floggerSchema.readlines():
#        print "Line is: ", line
        schemaStr += " %s" % line
#    print "schemaStr is: ", schemaStr
    try:
        cur.executescript(schemaStr)
    except Exception as e:
        # Failed to create flogger.db from schema, error
        print "Failed to create flogger.db from schema, error"
        return False
    floggerSchema.close()
    db.commit()
    db.close()
    print "opendb: OGN Databases built"
    return True

#-----------------------------------------------------------------
# Build flogger db using schema
#-----------------------------------------------------------------
#
cur = [0]    					# cur is mutable
schema="DBschema.sql"				# OGN database schema
r = opendb('DBschema.sql', cur)			# create the OGN database using the schema

conn=sqlite3.connect(r'OGN.db')			# connect now with the created database
curs=conn.cursor()

#####################				# add now the preset values into stations and receivers

addcmd="insert into STATIONS values (?,?,?,?)"
curs.execute(addcmd, ('LELT',  '990101', 1.0, 0))
curs.execute(addcmd, ('LEOC',  '990101', 1.0, 0))
curs.execute(addcmd, ('LEFM',  '990101', 1.0, 0))
curs.execute(addcmd, ('LECI1', '990101', 1.0, 0))
curs.execute(addcmd, ('LECI2', '990101', 1.0, 0))
curs.execute(addcmd, ('LETP',  '990101', 1.0, 0))
curs.execute(addcmd, ('LECD',  '990101', 1.0, 0))
curs.execute(addcmd, ('LEIG',  '990101', 1.0, 0))
curs.execute(addcmd, ('MORA',  '990101', 1.0, 0))
curs.execute(addcmd, ('CREAL', '990101', 1.0, 0))

conn.commit()
						# print the preset values as a way to check it
curs.execute ('select * from STATIONS')
for row in curs.fetchall():
    print row
conn.commit()
curs.execute ('select * from RECEIVERS')
for row in curs.fetchall():
    print row

print "Print dictionaries:"             
curs.execute('select * from STATIONS')
colnames = [desc[0] for desc in curs.description]
print "STATATIONS", colnames 
curs.execute('select * from RECEIVERS')
colnames = [desc[0] for desc in curs.description]
print "RECEIVERS", colnames
curs.execute('select * from OGNDATA')
colnames = [desc[0] for desc in curs.description]
print "OGNDATA", colnames
curs.execute('select * from GLIDERS')
colnames = [desc[0] for desc in curs.description]
print "GLIDERS", colnames
curs.execute('select * from METEO')
colnames = [desc[0] for desc in curs.description]
print "METEO", colnames
print "Database created .... "
conn.commit()
conn.close()

