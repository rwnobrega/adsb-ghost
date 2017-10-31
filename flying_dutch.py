# -*- coding: UTF-8 -*-
import json
import encoder
import adsb_dec
import util
from geopy.geocoders import Nominatim
import numpy


MOVEMENT_CONST = 0.0001
icao = "40621D"
lat_atual = -27.670118
lon_atual = -48.5481544
alts = '110000111000'
route = []
geolocator = Nominatim()
plan = open('flight_plan_binary.txt', 'w+')
lock = True

def travel(destination, alt, latitude=None, longitude=None, npoints=1):
    global city
    global icao
    global plan
    global lat_atual
    global lon_atual

    if (latitude == None and longitude == None):
        location = geolocator.geocode(destination, timeout=10)
        position_end = {"latitude" : location.latitude,
                        "longitude": location.longitude}
    else:
        position_end = {"latitude" : latitude,
                        "longitude": longitude}

    lat_list = numpy.linspace(position_init["latitude"], position_end["latitude"], npoints)
    lon_list = numpy.linspace(position_init["longitude"], position_end["longitude"], npoints)

    i = 0
    while i < len(lat_list):
        coordenadas = encoder.cpr_encode(lat_list[i], lon_list[i], 0, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position = encoder.aircraft_position('01011000', alt, latitude,
                                                     longitude, '0', icao)
        coordenadas = encoder.cpr_encode((lat_list[i] + MOVEMENT_CONST), (lon_list[i] + MOVEMENT_CONST), 1, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position1 = encoder.aircraft_position('01011000', alt, latitude,
                                                      longitude, '1', icao)
        plan.write(util.hex2bin(message_position))
        plan.write(util.hex2bin(message_position1))

        lat_atual = lat_list[i]
        lon_atual = lon_list[i]
        i = i + 1


list_command = []
list_value = []
dicts_from_file = []
with open('flight_plan.txt','r') as inf:
    for line in inf:
        dicts_from_file.append(eval(line))

while lock == True:

    for i in range(len(dicts_from_file)):
        position_init = {"latitude" : lat_atual,
                         "longitude": lon_atual}

        command = str(dicts_from_file[i].get('command'))
        command = command[2:len(command)-2]
        if i == (len(dicts_from_file) - 1):
            lock = False

        if command == 'travel':
            latitude = str(dicts_from_file[i].get('latitude'))
            latitude = latitude[1:len(latitude)-2]
            longitude = str(dicts_from_file[i].get('longitude'))
            longitude = longitude[1:len(longitude)-2]
            npoints = str(dicts_from_file[i].get('npoints'))
            npoints = npoints[1:len(npoints)-2]
            travel(None, alts, float(latitude), float(longitude), int(npoints))
        if command == 'name':
            name = str(dicts_from_file[i].get('name'))
            name = name[2:len(name)-2]
            message = encoder.aircraft_id(icao, name)
            plan.write(util.hex2bin(message))
        if command == 'alt':
            altura = str(dicts_from_file[i].get('altura'))
            altura = altura[1:len(altura)-1]
            alts = encoder.aircraft_altitude(int(altura))
            travel(None, alts)


plan.close()
b = open('flight_plan_binary.txt', "r")
c = b.readlines()
c = str(c)
c = c[2:(len(c)-2)]
chunks = [c[i:i+8] for i in range(0, len(c), 8)]
list_int = [int(x, 2) for x in chunks]
ba = bytearray(list_int)
f = open('final_plan.bin', 'wb')
f.write(ba)
f.close()
