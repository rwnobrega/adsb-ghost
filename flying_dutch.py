import json
import encoder
import adsb_dec
import gmplot
from termcolor import colored
from geopy.geocoders import Nominatim


MOVEMENT_CONST = 0.0001
icao = "40621D"
city = "Florianopolis"
alts = '110000111000'
route = []
geolocator = Nominatim()

# def sender(identifier, **payload_args):
#     return json.dumps([{'identifier': identifier, 'payload': payload_args}])
#     make_request(message_identifiers['call_transmit_request'],
#                         promise_id=promise_id,
#                         target=target,
#                         modules=modules)

def travel(destination, alt):
    global city
    global icao
    location = geolocator.geocode(destination, timeout=10)
    print("Voce quer ir: %s" % location.address)
    print("Latitude de destino: %s" % location.latitude)
    print("Longitude de destino:  %s" % location.longitude)

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

    gmap = gmplot.GoogleMapPlotter(-27.5973002, -48.5496098, 10)
    gmap.plot(lat_list, lon_list, 'cornflowerblue', edge_width=10)
    gmap.draw("map.html")
    i = 0
    while i < len(lat_list):
        coordenadas = encoder.cpr_encode(lat_list[i], lon_list[i], 0, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position = encoder.aircraft_position('01011000', alt, latitude, longitude, '0', icao)
        coordenadas = encoder.cpr_encode(lat_list[i+1], lon_list[i+1], 1, 1)
        latitude = encoder.get_lat(coordenadas)
        longitude = encoder.get_long(coordenadas)
        message_position1 = encoder.aircraft_position('01011000', alt, latitude, longitude, '1', icao)
        print colored(message_position.upper(), 'green')
        print colored(message_position1.upper(), 'red')
        coordenadas_dec = adsb_dec.position(message_position, message_position1, 1, 11)
        print coordenadas_dec
        i = i + 2
    city = destination

while True:
    location = geolocator.geocode(city, timeout=10)
    print("Voce esta em: %s" % location.address)
    print("Sua atual latitude: %s" % location.latitude)
    print("Sua atual longitude:  %s" % location.longitude)
    print("Sua atual altitude:  %s" % alts)

    position_init = {"latitude" : location.latitude,
                     "longitude": location.longitude}

    print "\n"
    print "travel - Set a travel command"
    print "name - change name"
    print "alt - Set altitude"
    print "exit - exit flying dutch\n\n"
    command = raw_input("What do you want to do? \n")
    if command == 'travel':
        destination = raw_input("Where u want to go? \n")
        travel(destination, alts)
    if command == 'name':
        name = raw_input("What is the name? \n")
        message = encoder.aircraft_id(icao, 'Flying_Dutch')
    if command == 'alt':
        alt = raw_input("What is the new alt? \n")
        print 'AQUI 1'
        alts = encoder.aircraft_altitude(int(alt))
        travel(city, alts)
    if command == 'exit':
        exit()
