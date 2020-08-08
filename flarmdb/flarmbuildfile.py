#!/usr/bin/python3
#
# Program to read flarm_id database and create a file as the base for known gliders
#

import string
import requests
import sys
import time
import sqlite3
import config
from tqdm import tqdm

import subprocess

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])




def flarmdb(prt, curs):

    global cin, cout, dups
    nlines = file_len("flarmdata.fln")
    db = open("flarmdata.fln", 'r')
    flm_txt = open("flarmdata.txt", 'w')
    # Read first line and convert to number
    x = db.readline()
    val = int(x, 16)
    print("First line from FlarmNet data is : ", val)

    i = 1
    line = ""
    nos_lines = val
    pbar = tqdm(total=nlines)               # indicate the total number of lines
    while True:
        # try:
        line = db.readline()
        if not line:
            return True
        pbar.update(1)
        line_lng = len(line)
        cin += 1
        string = ""
        for j in range(0, 172, 2):
            #            for j in range(0,line_lng - 1,2):
            #            x = line[j:j+2]
            #            y = int(x, 16)
            #            c = chr(y)
            c = chr(int(line[j:j+2], 16))
            string = string + c
        #print ("Rread: ", i, " Returns: ", line, string)
        i = i + 1
        ID = string[0:6]
        try:
            Airport = string[27:47]
            Airport = Airport.rstrip()
        except:
            print("Code error at Airport name:", str(string[27:47]))
            Airport = 'None'
        try:
            Type = string[48:69]
        except:
            print("Code error at Type:", str(string[48:69]))
            Type = 'None'
        Registration = string[69:75]
        Registration = Registration.strip("'")
        Registration = Registration.strip(" ")
        Registration = Registration.replace(" ", "_")
        Registration = Registration.replace(b'\xC2\x96'.decode('utf-8'), "-")

        try:
            Radio = string[79:86]
        except:
            print("Code error at Radio:", str(string[79:86]))
            Radio = 'None'
        if prt:
            print("Line: ", i-1, " ID: ", ID,  " Airport: ", Airport, " Type: ",
                  Type, " Registration: ", Registration,  " Radio: ", Radio)
        # write just what we need: ID and registration
        row = '\t\t"%s":"%s",\n' % (ID,  Registration)
        ID = ID.strip("'").upper()
        Registration = Registration.strip("'")
        Type = Type.strip("'")
        try:
            curs.execute("insert into GLIDERS values(?,?,?,?,?,?)",
                         (ID, Registration, " ", Type, "F", "F"))
            flm_txt.write(row)
            cout += 1
        except:
            dups += 1
            if prt:
                print ("Duplicate ID on DB:", ID,
                       Registration, Type, "Dup #", dups, i-1)
        # except:
        #print("Error at row : ", i - 1)
        # return True
    pbar.close()
    return True
#
# Main logic
#


cin = 0
cout = 0
dups = 0
prtreq = sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False
print("\n\nStart build Flarm file from Flarmnet")
filedb=config.DBpath+config.SQLite3
print ("Updating SQLite3 DB:", filedb)
conn = sqlite3.connect(filedb)
curs = conn.cursor()

t1 = time.time()
flarmdb(prt, curs)

print("Input:", cin, "Output:", cout, "Dups:", dups)
t2 = time.time()
print("End build FlarmNET DB in ", t2 - t1, " seconds\n\n")
conn.commit()
conn.close()
