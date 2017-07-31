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

    def aircraft_position(self, SS):
            DF = '11' #Downforlmat
            TC = '12' #Typecode of message
            SS =  '00' #Surveillance status
            msg = DF + TC + SS + NICsb + ALT + T + F + LAT_CPR + LON_CPR
encoder = Encoder()
message2send0 = encoder.aircraft_position('00')
message2send = encoder.aircraft_id('4840D6', 'TESTEFLY')
print("Downlink format: %s " % adsb_dec.df(message2send))
print("ICAO aircraft address: %s " % adsb_dec.icao(message2send))
print("Message data: %s " % adsb_dec.data(message2send))
print("Type code: %s " % adsb_dec.typecode(message2send))
if adsb_dec.typecode(message2send) <= 4 and adsb_dec.typecode(message2send) >= 1:
    print("###########################  Aircraft ID Message #############################")
    print("Aircraft callsign: %s " % adsb_dec.callsign(message2send))
    print("Aircraft category number: %s" % adsb_dec.category(message2send))
if adsb_dec.typecode(message2send) <= 18 and adsb_dec.typecode(message2send) >= 9:
    print("########################### Airborne Positions Message #############################")
