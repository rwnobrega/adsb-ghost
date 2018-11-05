# -*- coding: UTF-8 -*-
import json
import encoder
import adsb_dec
import util


MOVEMENT_CONST = 0.0001
icao = "40621D"
alts = '110000111000'
plan = open('flight_plan_binary.txt', 'w+')
lock = True

current_latitude = -27.608339
current_longitude = -48.633269

def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def travel(coordinates, alt, icao, current_latitude, current_longitude):
    global plan

    lat_list = []
    lon_list = []

    lat_list.append(current_latitude)
    lon_list.append(current_longitude)
    lat_list.append(current_latitude + MOVEMENT_CONST)
    lon_list.append(current_longitude + MOVEMENT_CONST)

    lat_list.append(coordinates['latitude'])
    lon_list.append(coordinates["longitude"])
    lat_list.append(coordinates["latitude"] + MOVEMENT_CONST)
    lon_list.append(coordinates["longitude"] + MOVEMENT_CONST)

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

        print(message_position)
        print(message_position1)
        print("\n")
        # print(util.hex2bin(message_position))
        # print((util.hex2bin(message_position1)))

        plan.write(util.hex2bin(message_position))
        plan.write(util.hex2bin(message_position1))

        # coordenadas_dec = adsb_dec.position(message_position,
        #                                     message_position1, 1, 11)
        # print(coordenadas_dec)
        i = i + 2


flight_plan = open("flight_plan.txt","r")
a = flight_plan.readlines()
list_command = []
list_value = []
for i in range(len(a)):
    b = a[i].split(";")
    list_command.append(b[0])
    list_value.append(b[1].rstrip())

while lock == True:

    for i in range(len(a)):

        if i == (len(a) - 1):
            lock = False

        if list_command[i] == 'travel':

            destiny_coordinates = list_value[i].split(",")
            destiny_coordinates = {'latitude': float(destiny_coordinates[0]),
                           'longitude': float(destiny_coordinates[1])}

            travel(destiny_coordinates, alts, icao, current_latitude, current_longitude)
        # if list_command[i] == 'name':
        #     message = encoder.aircraft_id(icao, 'Flying_Dutch')
        # if list_command[i] == 'alt':
        #     alts = encoder.aircraft_altitude(int(list_value[i]))
        #     travel(alts)

plan.close()
#
b = open('flight_plan_binary.txt', "r")
c = b.readlines()
c = str(c)
c = c[2:(len(c)-2)]
chunks = [c[i:i+8] for i in range(0, len(c), 8)]
list_int = [int(x, 2) for x in chunks]
ba = bytearray(list_int)

binary_packet = []
for i in  ba:
    binary_packet.append('{0:08b}'.format(i))


packets = []
for packet in range(8, len(binary_packet), 14):
    packets.append(binary_packet[(packet - 8):packet])

packets_formated = []
for i in packets:
    packets_formated.append(concatenate_list_data(i))

print(len(packets_formated))
for i in packets_formated:
    print(i)
    print(len(i))
