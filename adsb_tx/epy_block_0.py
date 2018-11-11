"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import encoder
import util
from gnuradio import gr
from subprocess import call

MOVEMENT_CONST = 0.0001
class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""


        gr.basic_block.__init__(
            self,
            name='ADSB encoder',   # will show up in GRC
            in_sig=[],
            out_sig=[np.uint8]
        )

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

	self.int_to_return = []

    def travel(self, coordinates, alt, icao, current_latitude, current_longitude, plan = None):

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
            plan.write(util.hex2bin(message_position))
            plan.write(util.hex2bin(message_position1))

            # coordenadas_dec = adsb_dec.position(message_position,
            #                                     message_position1, 1, 11)
            i = i + 2

    def general_work(self, input_items, output_items):
        if not self.int_to_return:
            icao = "40621D"
            alts = '110000111000'
            plan = open('/home/llucindov/dev/telecom/adsb-ghost/flight_plan_binary.txt', 'w+')
            lock = True
            current_latitude = -27.608339
            current_longitude = -48.633269
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
                        self.travel(destiny_coordinates, alts, icao, current_latitude, current_longitude, plan)

                    if list_command[i] == 'name':
                        message = encoder.aircraft_id(icao, list_value[i])
                        plan.write(util.hex2bin(message))

                    # if list_command[i] == 'alt':
                    #     destiny_coordinates = {'latitude': current_latitude,'longitude': current_longitude}
                    #     alts = encoder.aircraft_altitude(int(list_value[i]))
                    #     self.travel(self, destiny_coordinates, alts, message, current_latitude, current_longitude, plan)

            plan.close()
            b = open('/home/llucindov/dev/telecom/adsb-ghost/flight_plan_binary.txt', "r")
            c = b.readlines()
            c = str(c)
            c = c[2:(len(c)-2)]

            chunks = [c[i:i+8] for i in range(0, len(c), 8)]
            list_int = [int(x, 2) for x in chunks]
            self.int_to_return = list_int
            output_items[0][0] = self.int_to_return.pop(0)
            return 1

        else:
            if self.int_to_return:
                output_items[0][0] = self.int_to_return.pop(0)
                return 1
