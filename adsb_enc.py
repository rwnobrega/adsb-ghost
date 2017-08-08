# Copyright (C) 2015 Junzi Sun (TU Delft)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A python package for encoding ADS-B messages.
"""

import math
import util
import adsb_dec


class Encoder():

    def __init__(self):
        self.lat_zones = 15
        self.nb = 17
        self.evenlist = {}
        self.oddlist = {}
        self.nl_table = None
        self.lat_limit = [0]*60
        self.lat_limits()
        self.nl_tables()

    def lat_limits(self):
        self.lat_limit[1] = 90
        for i in xrange(2, 4*self.lat_zones-1 + 1):
            self.lat_limit[i] = int(round((180/math.pi) * math.acos(math.sqrt
                                    ((1-math.cos(math.pi/(2.*15)))/(1-math.cos
                                     (2*math.pi/i))))))

    def nl_tables(self):
        self.nl_table = [0] * 91
        for declat_in in self.lat_limit[1:]:
            for j in range(declat_in, 0, -1):
                if j >= 87 or j == 0:
                    continue
                self.nl_table[j] = int(math.floor((2.0*math.pi)/math.acos(1.0 -
                                       (1.0 - math.cos(math.pi / (2.0 *
                                        self.lat_zones))) / math.cos((math.pi /
                                         180.0) * abs(j))**2)))
                assert self.nl_table[j] in xrange(1, 60)

    def nl(self, declat_in):
        declat_in_ = abs(int(math.floor(declat_in)))
        if declat_in_ == 0:
            return 59
        if declat_in_ == 87:
            return 2
        if declat_in_ > 87:
            return 1
        return self.nl_table[declat_in_]

    def rlat(self, declat, lon):
        return int((360/(4*self.lat_zones)) * (1.*lon/(2**self.nb) +
                   math.floor(1.*declat/(360/(4*self.lat_zones)))))

    def cpr_encode(self, lat, lon):
        tmp = 360
        dlat = 360/(4*self.lat_zones)
        latitude = int(math.floor(2**self.nb*(lat % dlat) / dlat + 0.5))
        cond = self.nl(self.rlat(lat, latitude))
        if cond > 0:
            tmp = 360 / cond
        dlon = tmp
        longitude = int(math.floor(2**self.nb * (lon % dlon) / dlon + 0.5))
        return (latitude, longitude)

    def aircraft_id(self, icao, data):
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

    def aircraft_position(self, TC_SS_NICsb, ALT, LAT_CPR, LON_CPR, flag):
        DF = '10001'
        ALT = ALT
        T = '0'
        F = flag
        LAT_CPR = LAT_CPR
        LON_CPR = LON_CPR
        x = (DF, TC_SS_NICsb, ALT, T, F, LAT_CPR, LON_CPR)
        msg = ("").join(x)
        return msg


encoder = Encoder()
coordenadas = encoder.cpr_encode(52.25720, 3.91937)
latitude = bin(coordenadas[0])
longitude = bin(coordenadas[1])
latitude = latitude.split("0b")
longitude = longitude.split("0b")
latitude = latitude[1]
longitude = longitude[1]
print latitude
print longitude
message_position = encoder.aircraft_position('01011000', '110000111000',
                                             latitude, longitude, '0')
message_position1 = encoder.aircraft_position('01011000', '110000111000',
                                              '10010000110101110',
                                              '01100010000010010', '1')
print('Message Position is: %s' % message_position)
print('Message Position is: %s' % message_position1)
print(adsb_dec.airborne_position(message_position, message_position1, 1, 11))


# message_id = encoder.aircraft_id('4840D6', 'TESTEFLY')
# print("Downlink format: %s " % adsb_dec.df(message_id))
# print("ICAO aircraft address: %s " % adsb_dec.icao(message_id))
# print("Message data: %s " % adsb_dec.data(message_id))
# print("Type code: %s " % adsb_dec.typecode(message_id))
# if adsb_dec.typecode(message_id) <= 4 and adsb_dec.typecode(message_id) >= 1:
#     print("###########################  Aircraft ID Message ############")
#     print("Aircraft callsign: %s " % adsb_dec.callsign(message_id))
#     print("Aircraft category number: %s" % adsb_dec.category(message_id))
# if adsb_dec.typecode(message_id) <= 18 and adsb_dec.typecode(message_id)>=9:
#     print("########################### Airborne Positions Message #########")
