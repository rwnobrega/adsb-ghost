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

def callsign(icao, data):
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

print(callsign('4840D6', 'TESTEFLY'))
