import math, time
import adsb_dec
import util

latz = 15

# def aircraft_velocity(TC = '10011', ST = '001', IC = '0', RESV_A = '1', NAC = '000', S_EW, V_EW, S_NS, V_NS,
#                      VrSrc, S_Vr, Vr, RESV_B = '00', S_Dif, Dif):
#
#     # TC -> 10011 (19) - Type Code
#     # ST -> 001 (ground velocity - Subtype)
#     # IC -> 0 (Intent change flag)


def aircraft_altitude(altitude_new):
    #TODO Ver arredondamento
    alt = (altitude_new + 1000)/25
    alt_bin = bin(alt)
    altitude = alt_bin.split("0b")
    altitude = altitude[1]
    if len(altitude) is not 11:
        while len(altitude) < 11:
            altitude = '0' + altitude
    altitude_1 = altitude[0:7] + '1' + altitude[7:12]
    if len(altitude_1) is not 12:
        print "U cant send this message, man"
        return '000000000000'
    return altitude_1

def aircraft_id(icao, data):
    """Aircraft ID

    Args:
        icao (6-character hexstring): ICAO24 aircraft type
        data (8-character hexstring): aircraft ID.

    Returns:
    ADS-B packet: 28-character hexstring

    """
    chars = '#ABCDEFGHIJKLMNOPQRSTUVWXYZ#####_###############0123456789######'
    dfca = '8D'
    data_int_list = [chars.index(x) for x in data]
    data_bin = ''.join('{0:06b}'.format(x) for x in data_int_list)
    data_hex = '{0:012X}'.format(int(data_bin, 2))
    msg0 = dfca + icao + '20' + data_hex
    crc = '{0:06X}'.format(int(util.crc(msg0 + '000000', encode=True), 2))
    return msg0 + crc

def aircraft_position(TC_SS_NICsb, ALT, LAT_CPR, LON_CPR, flag, icao):
    dfca = '8D'
    ALT = ALT
    T = '0'
    F = flag
    LAT_CPR = LAT_CPR
    LON_CPR = LON_CPR
    package =  '0b' + TC_SS_NICsb + ALT + T + F + LAT_CPR + LON_CPR
    package = hex(int(package, 2))
    package = package.split("0x")
    package = package[1]
    msg = dfca + icao + package
    crc = '{0:06X}'.format(int(util.crc(msg + '000000', encode=True), 2))
    return msg + crc

def get_lat(coordenadas):
    latitude_bin = bin(coordenadas[0])
    latitude = latitude_bin.split("0b")
    latitude = latitude[1]
    if len(latitude) is not 17:
        while len(latitude) < 17:
            latitude = '0' + latitude
    return latitude

def get_long(coordenadas):
    longitude_bin = bin(coordenadas[1])
    longitude = longitude_bin.split("0b")
    longitude = longitude[1]
    if len(longitude) is not 17:
        while len(longitude) < 17:
            longitude= '0' + longitude
    return longitude

def nz(ctype):
    return 4 * latz - ctype

def dlat(ctype):
	nzcalc = nz(ctype)
	if nzcalc == 0:
		return 360.0
	else:
		return 360.0 / nzcalc

def nl(declat_in):
	if abs(declat_in) >= 87.0:
		return 1.0
	return math.floor( (2.0*math.pi) * math.acos(1.0- (1.0-math.cos(math.pi/(2.0*latz))) / math.cos( (math.pi/180.0)*abs(declat_in) )**2 )**-1)

def dlon(declat_in, ctype):
	nlcalc = max(nl(declat_in)-ctype, 1)
	return 360.0 / nlcalc

def cpr_encode(lat, lon, ctype, surface):
	if surface is True:
		scalar = 2.**19
	else:
		scalar = 2.**17

	dlati = dlat(ctype)
	yz = math.floor(scalar * ((lat % dlati)/dlati) + 0.5)
	rlat = dlati * ((yz / scalar) + math.floor(lat / dlati))

	dloni = dlon(lat, ctype)
	xz = math.floor(scalar * ((lon % dloni)/dloni) + 0.5)

	yz = int(yz) & (2**17-1)
	xz = int(xz) & (2**17-1)

	return (yz, xz) #lat, lon
