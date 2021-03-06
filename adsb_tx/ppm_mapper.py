import numpy as np
from gnuradio import gr


class blk(gr.interp_block):

    def __init__(self):
        gr.interp_block.__init__(
            self,
            name='PPM mapper',
            in_sig=[np.int8],
            out_sig=[np.int32],
            interp=2
        )

    def work(self, input_items, output_items):
        for i, b in enumerate(input_items[0]):
            output_items[0][2*i] = b
            output_items[0][2*i + 1] = not b
        return len(output_items[0])
