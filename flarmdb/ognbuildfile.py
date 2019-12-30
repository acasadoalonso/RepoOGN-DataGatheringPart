#!/usr/bin/python3
#
# Program to read OGN  database and create a file as the base for known gliders
#

import string
import requests
import time
import sys
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



def isprintable(s, codec='latin1'):
    try:
        s.decode(codec)
    except UnicodeDecodeError:
        return False
    else:
        return True


def ogndb(prt, curs):

    nlines  = file_len("ognddbdata.csv")        # input file
    db      = open("ognddbdata.csv", 'r')       # input file
    flm_txt = open("ognddbdata.txt", 'w')       # output file

    print("Process the OGN Device Database - DDB")
    line = db.readline().encode("latin1")
    if prt:
        print("Format: ", line)
    i = 1
    line = ""
    pbar = tqdm(total=nlines)               # indicate the total number of lines 

    while True:
        try:
            line = db.readline().encode("latin1")
        except UnicodeDecodeError:
            continue
        line_lng = len(line)
        if line_lng == 0:
            return (i-1)
        pbar.update(1) 
        string = ""
        if prt:
            print("read: ", i, " returns: ", line, "of ", nlines)
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
        row = '\t\t%s : %s,\t\t # %s # %s # %s # \n' % (ID,  Registration, model, cn, device)
        flm_txt.write(row)
        device = device.strip("'")
        ID = ID.strip("'")
        Registration = Registration.strip("'")
        cn = cn.strip("'")
        model = model.strip("'")

        curs.execute("insert into GLIDERS values(?,?,?,?,?, ?)", (ID, Registration, cn, model, "O", device))
        if prt:
            print(ID, Registration, cn, model)
    pbar.close()
    return (nlines)

#
# Main logic
#
prtreq = sys.argv[1:]
if prtreq and prtreq[0] == 'prt':
    prt = True
else:
    prt = False
filedb=config.DBpath+config.SQLite3
conn = sqlite3.connect(r'/nfs/OGN/DIRdata/OGN.db')
curs = conn.cursor()
curs.execute("delete from GLIDERS")             # delete all rows

print("Start build the OGN file from OGN device database")
t1 = time.time()
nlines=ogndb(prt, curs)
print("\n\n\nNumber of rows is: ", nlines)
t2 = time.time()
print("End build OGN DB in ", t2 - t1, " seconds")
conn.commit()
