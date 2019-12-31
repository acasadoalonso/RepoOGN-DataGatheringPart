import sqlite3
import config
def opendb (schema_file, cursor):
    # Open a connection to the database
    # Build the database from the supplied schema
    dbfile=config.DBpath+config.SQLite3
    print("opendb:", dbfile)
    try:
        db = sqlite3.connect(dbfile)
    except Exception as e:
        # Failed to open flogger.db, error
        print("Failed to open SAROGN.db, error")
        return False
    
    # Create a cursor to work with
    cur = db.cursor()
    cursor[0] = cur
    
    # Drop tables if they exist in the database 
    floggerSchema = open(schema_file)
    print(("opendb:", schema_file, " open ok"))
    schemaStr = ""
    for line in floggerSchema.readlines():
#        print "Line is: ", line
        schemaStr += " %s" % line
#    print "schemaStr is: ", schemaStr
    try:
        cur.executescript(schemaStr)
    except Exception as e:
        # Failed to create flogger.db from schema, error
        print("Failed to create flogger.db from schema, error")
        return False
    floggerSchema.close()
    db.commit()
    db.close()
    print("opendb: OGN Databases built")
    return True

