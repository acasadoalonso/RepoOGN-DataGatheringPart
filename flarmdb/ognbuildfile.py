#!/usr/bin/python3
#
# Program to read OGN  database and create a file as the base for known gliders
#

import string
import requests
import time
import sys
import sqlite3


def isprintable(s, codec='latin1'):
    try:
        s.decode(codec)
    except UnicodeDecodeError:
        return False
    else:
        return True


def ogndb(prt, curs):

    db = open("ognddbdata.csv", 'r')
    flm_txt = open("ognddbdata.txt", 'w')

    print("Process OGN database")
    line = db.readline().encode("latin1")
    if prt:
        print("Format: ", line)
    i = 1
    line = ""

    while True:
        try:
            line = db.readline().encode("latin1")
        except UnicodeDecodeError:
            continue
        line_lng = len(line)
        if line_lng == 0:
            print("\nNumber of rows is: ", i - 1)
            return True
        string = ""
        if prt:
            print("read: ", i, " returns: ", line)
        fil = line.decode('utf-8').split(',')
        device = fil[0]
        ID = fil[1]
        model = fil[2]
        if model == None:
            model = ' '
        Registration = fil[3]
        if Registration == None or Registration == "''":
            Registration = "'NOREG'"
        cn = fil[4]
        if cn == None:
            cn = ' '
        i = i + 1
        if prt:
            print("Line: ", i-1, " ID: ", ID,  " Dev: ", device, " Model: ", model, " Registration: ", Registration,  " CN: ", cn)
        Registration = Registration.strip(" ")
        Registration = Registration.replace(" ", "_")
        # write just what we need: ID and registration
        row = '\t\t%s : %s,\n' % (ID,  Registration)
        flm_txt.write(row)
        device = device.strip("'")
        ID = ID.strip("'")
        Registration = Registration.strip("'")
        cn = cn.strip("'")
        model = model.strip("'")

        curs.execute("insert into GLIDERS values(?,?,?,?,?, ?)",
                     (ID, Registration, cn, model, "O", device))
        if prt:
            print(ID, Registration, cn, model)


#
# Main logic
#
prtreq = sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False
conn = sqlite3.connect(r'/nfs/OGN/DIRdata/OGN.db')
curs = conn.cursor()
curs.execute("delete from GLIDERS")             # delete all rows

print("Start build OGN file from OGN database")
t1 = time.time()
ogndb(prt, curs)
t2 = time.time()
print("End build OGN DB in ", t2 - t1, " seconds")
conn.commit()
