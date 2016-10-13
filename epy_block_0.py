"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.interp_block.__init__(
            self,
            name='PPM mapper',   # will show up in GRC
            in_sig=[np.int32],
            out_sig=[np.int32],
            interp=2
        )

    def work(self, input_items, output_items):
        for i, b in enumerate(input_items[0]):
            output_items[0][2*i] = b
            output_items[0][2*i + 1] = not b
        return len(output_items[0])
