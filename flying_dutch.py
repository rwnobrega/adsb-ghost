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
city = "Aeroporto Hercilio Luz - Florianopolis"
alts = '110000111000'
route = []
geolocator = Nominatim()
plan = open('flight_plan_binary.txt', 'w+')
lock = True
lat_list_plot = []
lon_list_plot = []

def travel(destination, alt):
    global city
    global icao
    global plan
    global lat_list_plot
    global lon_list_plot
    location = geolocator.geocode(destination, timeout=10)

    position_end = {"latitude" : location.latitude,
                    "longitude": location.longitude}

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
        i = i + 2
    city = destination


flight_plan = open("flight_plan.txt","r")
a = flight_plan.readlines()
list_command = []
list_value = []
for i in range(len(a)):
    b = a[i].split("-")
    list_command.append(b[0])
    list_value.append(b[1].rstrip())

while lock == True:

    for i in range(len(a)):
        location = geolocator.geocode(city, timeout=10)
        position_init = {"latitude" : location.latitude,
                         "longitude": location.longitude}
        if i == (len(a) - 1):
            lock = False
        if list_command[i] == 'travel':
            travel(list_value[i], alts)
        if list_command[i] == 'name':
            message = encoder.aircraft_id(icao, 'Flying_Dutch')
        if list_command[i] == 'alt':
            alts = encoder.aircraft_altitude(int(list_value[i]))
            travel(city, alts)

gmap = gmplot.GoogleMapPlotter(-27.5973002, -48.5496098, 10)
gmap.plot(lat_list_plot, lon_list_plot, 'cornflowerblue', edge_width=5)
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
