from geoip import geolite2

def geolocate(ip):
    match = geolite2.lookup(ip)
    geostr = None
    if match is not None:
        geostr = match.timezone
    return geostr
