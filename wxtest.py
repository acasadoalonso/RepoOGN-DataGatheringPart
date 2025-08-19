#
# gather the WX record from the APRS file and decode it
#

# example:   grep OGNDVS /nfs/OGN/DIRdata/DATA* | grep LEZS | tail -n 20 | python ~/src/SARsrc/wxtest.py



from parserfuncs import parseraprs
import fileinput
msg={}

for line in fileinput.input():
    #print ("LLL:", line)
    parseraprs(line, msg)
    if msg['source'] != 'WTX':			# if not weather ignore it
       continue

    #print ("MMM", msg)
    tempf=msg['temp']
    humidity=msg['humidity']
    rain=msg['rain']
    if tempf != ' ':
       tempc = round((float(tempf)-32)*5/9, 2)
    else:
       tempc=0.0
    message=""
    if tempc != 0.0:
       message += " Temp: %.2fºC"%tempc
    if humidity != ' ':
       message +=  " Humidity: "+msg['humidity']+"%"
    if rain != ' ':
       message +=  " Rain: "+msg['rain']+"%"
    print ("Station:", msg['station'], "Time (UTC):", msg['otime'], "Wind (dir/spd/burst):", msg['windspeed'], message)


