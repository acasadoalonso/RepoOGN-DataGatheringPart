import datetime
def get_longitude(packet):
    try:
        longitude=packet[0].longitude[0]
    except ValueError:
        longitude = -1
    return longitude

def get_latitude(packet):
    try:
        latitude=packet[0].latitude[0]
    except ValueError:
        latitude = -1
    return latitude

def get_altitude(packet):
    try:
        altitude=packet[0].altitude[0]
    except ValueError:
        altitude = -1
    return altitude

def get_speed(packet):
    try:
        speed=packet[0].speed[0]
    except ValueError:
        speed = -1
    return speed

def get_course(packet):
    try:
        course=packet[0].course[0]
    except ValueError:
        course = -1
    return course

def get_path(packet):
    try:
        path=packet[0].path[0]
    except ValueError:
        path = -1
    return path

def get_type(packet):
    try:
        type=packet[0].type[0]
    except ValueError:
        type = -1
    return type

def get_dst_callsign(packet):
    try:
        dst_callsign=packet[0].dst_callsign
    except ValueError:
        dst_callsign = ''
    return dst_callsign

def get_destination(packet):
    try:
        destination=packet[0].destination
    except ValueError:
        destination = ''
    return destination

def get_header(packet):
    try:
        header=packet[0].header
    except ValueError:
        header = ''
    return header

def get_otime(packet):
    try:
        itime=packet[0].timestamp[0]
        otime=datetime.datetime.utcfromtimestamp(itime)
    except ValueError:
        otime = 0
    return otime
