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
import adsb_dec

MOVEMENT_CONST = 0.0001
class blk(gr.basic_block):

    def __init__(self):

        gr.basic_block.__init__(
            self,
            name='ADSB encoder',
            in_sig=[],
            out_sig=[np.uint8]
        )
        self.sign_NS = ''
        self.sign_LO = ''
        self.n_points = 0
        self.int_to_return = []
        self.current_latitude = 0
        self.current_longitude = 0

    def travel(self, coordinates, alt, icao, plan = None):

        lat_list = []
        lon_list = []


        lat_list.append(self.current_latitude)
        lon_list.append(self.current_longitude)

        lat_list.append(self.current_latitude + MOVEMENT_CONST)
        lon_list.append(self.current_longitude + MOVEMENT_CONST)


        lat_list = np.linspace(self.current_latitude, coordinates["latitude"], self.n_points).tolist()
        lon_list = np.linspace(self.current_longitude, coordinates["longitude"], self.n_points).tolist()


        i = 0

        while i < len(lat_list):

            coordenadas = encoder.cpr_encode(lat_list[i], lon_list[i], 0, 1)
            latitude =  encoder.get_lat(coordenadas)
            longitude = encoder.get_long(coordenadas)
            self.current_latitude = lat_list[i]
            self.current_longitude = lon_list[i]
            message_position = encoder.aircraft_position('01011000', alt, latitude,
                                                         longitude, '0', icao)

            coordenadas = encoder.cpr_encode(lat_list[i+1], lon_list[i+1], 1, 1)
            latitude = encoder.get_lat(coordenadas)
            longitude = encoder.get_long(coordenadas)
            message_position1 = encoder.aircraft_position('01011000', alt, latitude,
                                                          longitude, '1', icao)

            message_velocity = encoder.aircraft_velocity(icao, self.sign_LO, self.v_lo , self.sign_NS, self.v_ns)
            # print(adsb_dec.position(message_position, message_position1, 1, 11))
            # print(adsb_dec.velocity(message_velocity))
            # print("ENVIADO1: ",message_position)
            # print("ENVIADO2: ",message_position1)
            plan.append(util.hex2bin(message_position))
            plan.append(util.hex2bin(message_position1))
            plan.append(util.hex2bin(message_velocity))

            i = i + 2

    def general_work(self, input_items, output_items):
        if not self.int_to_return:
            icao = "40621D"
            alts = '110000111000'
            plan = []
            lock = True
            flight_plan = open("/home/llucindov/dev/telecom/adsb-ghost/flight_plan.txt","r")
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

                    if list_command[i] == 'set_position':
                        current_coordinates = list_value[i].split(",")
                        self.current_latitude = float(current_coordinates[0])
                        self.current_longitude = float(current_coordinates[1])


                    if list_command[i] == 'travel':
                        values = list_value[i].split(",")
                        destiny_coordinates = {'latitude': float(values[0]),
                                               'longitude': float(values[1])}

                        self.n_points = float(values[2])

                        if self.current_longitude > float(values[1]):
                            self.sign_NS = '1'
                        else:
                            self.sign_NS = '0'

                        if self.current_latitude > float(values[0]):
                            self.sign_LO = '1'
                        else:
                            self.sign_LO = '0'

                        self.v_lo = '{0:010b}'.format(int(values[3]))
                        self.v_ns = '{0:010b}'.format(int(values[4]))

                        self.travel(destiny_coordinates, alts, icao, plan)


                    if list_command[i] == 'name':
                        message = encoder.aircraft_id(icao, list_value[i])
                        plan.append(util.hex2bin(message))

            c = ''
            for item in plan:
                c = c + item

            chunks = [c[i:i+8] for i in range(0, len(c), 8)]
            list_int = [int(x, 2) for x in chunks]
            self.int_to_return = list_int
            output_items[0][0] = self.int_to_return.pop(0)
            return 1

        else:
            if self.int_to_return:
                output_items[0][0] = self.int_to_return.pop(0)
                return 1
