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
        msg0 = dfca + icao + '20' + data_hex #"20" is the type code
        crc = '{0:06X}'.format(int(util.crc(msg0 + '000000', encode=True), 2))
        return msg0 + crc

    def aircraft_position(self, TC_SS_NICsb , ALT, LAT_CPR, LON_CPR):
            DF = '11' #Downformat
            ALT = ALT #Altitude
            T = '0' #Time
            F = '0' #CPR odd/even frame flag
            LAT_CPR = LAT_CPR #Latitude in CPR format
            LON_CPR = LON_CPR #Longitude in CPR format
            msg = DF + TC_SS_NICsb + ALT + T + F + LAT_CPR + LON_CPR
            return msg

encoder = Encoder()
message_position = encoder.aircraft_position('58', 'C38', '16B48', 'C8AC')
print('Message Position is: %s' % message_position)

message_id = encoder.aircraft_id('4840D6', 'TESTEFLY')
print("Downlink format: %s " % adsb_dec.df(message_id))
print("ICAO aircraft address: %s " % adsb_dec.icao(message_id))
print("Message data: %s " % adsb_dec.data(message_id))
print("Type code: %s " % adsb_dec.typecode(message_id))
if adsb_dec.typecode(message_id) <= 4 and adsb_dec.typecode(message_id) >= 1:
    print("###########################  Aircraft ID Message #############################")
    print("Aircraft callsign: %s " % adsb_dec.callsign(message_id))
    print("Aircraft category number: %s" % adsb_dec.category(message_id))
if adsb_dec.typecode(message_id) <= 18 and adsb_dec.typecode(message_id) >= 9:
    print("########################### Airborne Positions Message #############################")
