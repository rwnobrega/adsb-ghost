# -*- coding: UTF-8 -*-
import json
import encoder
import adsb_dec
import gmplot
import util
from termcolor import colored
from geopy.geocoders import Nominatim


MOVEMENT_CONST = 0.0001
icao = "40621D"
lat_atual = -27.670118
lon_atual = -48.5481544
alts = '110000111000'
route = []
geolocator = Nominatim()
plan = open('flight_plan_binary.txt', 'w+')
lock = True
lat_list_plot = []
lon_list_plot = []

def travel(destination, alt, latitude=None, longitude=None):
    global city
    global icao
    global plan
    global lat_list_plot
    global lon_list_plot

    if (latitude == None and longitude == None):
        location = geolocator.geocode(destination, timeout=10)
        position_end = {"latitude" : location.latitude,
                        "longitude": location.longitude}
    else:
        position_end = {"latitude" : latitude,
                        "longitude": longitude}

    lat_list = []
    lon_list = []

    lat_list.append(position_init["latitude"])
    lon_list.append(position_init["longitude"])
    lat_list.append(position_init["latitude"] + MOVEMENT_CONST)
    lon_list.append(position_init["longitude"] + MOVEMENT_CONST)

    lat_list.append(position_end["latitude"])
    lon_list.append(position_end["longitude"])
    lat_list.append(position_end["latitude"] + MOVEMENT_CONST)
    lon_list.append(position_end["longitude"] + MOVEMENT_CONST)

    lat_list_plot.append(position_init["latitude"])
    lon_list_plot.append(position_init["longitude"])
    lat_list_plot.append(position_init["latitude"] + MOVEMENT_CONST)
    lon_list_plot.append(position_init["longitude"] + MOVEMENT_CONST)

    lat_list_plot.append(position_end["latitude"])
    lon_list_plot.append(position_end["longitude"])
    lat_list_plot.append(position_end["latitude"] + MOVEMENT_CONST)
    lon_list_plot.append(position_end["longitude"] + MOVEMENT_CONST)

    i = 0
    while i < len(lat_list):
        coordenadas = encoder.cpr_encode(lat_list[i], lon_list[i], 0, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position = encoder.aircraft_position('01011000', alt, latitude,
                                                     longitude, '0', icao)
        coordenadas = encoder.cpr_encode(lat_list[i+1], lon_list[i+1], 1, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position1 = encoder.aircraft_position('01011000', alt, latitude,
                                                      longitude, '1', icao)
        plan.write(util.hex2bin(message_position))
        plan.write(util.hex2bin(message_position1))
        coordenadas_dec = adsb_dec.position(message_position,
                                            message_position1, 1, 11)
        lat_atual = lat_list[i]
        lon_atual = lon_list[i]
        i = i + 2
    print "LATITUDE ATUAL"
    print lat_atual
    print "LONGITUDE ATUAL"
    print lon_atual

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
            travel(None, alts, float(latitude), float(longitude))
        if command == 'name':
            message = encoder.aircraft_id(icao, 'Flying_Dutch')
        if command == 'alt':
            altura = str(dicts_from_file[i].get('altura'))
            altura = altura[1:len(altura)-1]
            print altura
            alts = encoder.aircraft_altitude(int(altura))
            travel(city, alts)

gmap = gmplot.GoogleMapPlotter(-27.5973002, -48.5496098, 10)
gmap.plot(lat_list_plot, lon_list_plot, 'cornflowerblue', edge_width=10)
gmap.draw("trajetoria.html")
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
