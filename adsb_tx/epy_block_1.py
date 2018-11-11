"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ADSB DECODER',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.packet = ''


    def work(self, input_items, output_items):

        if len(input_items[0]) < 112:
            return 0

        for i in input_items[0]:
            self.packet = self.packet + str(input_items[0][i].astype(int))

        if len(self.packet) > 112:
            packet = self.packet[0:112]
            print("PACOTE: ", self.packet)
            self.packet = self.packet[113:]

        self.consume(0, len(input_items[0]))
        return 0
