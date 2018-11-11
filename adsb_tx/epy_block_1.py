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

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ADSB DECODER',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param


    def forecast(self, noutput_items, ninput_items_required):
        ninput_items_required = 14

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        # print((input_items[0][0:112]))
        # print(len(input_items[0][0:112]))

        self.consume(0, 8)
        return 0
