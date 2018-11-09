"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Decoder',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # self.preambule = '1010000101000000'
        self.preambule = '1010000101000000'
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def general_work(self, input_items, output_items):

        if len(input_items[0]) < 128:
            return 0

        retorno = 0
        n_sample = 6
        samples = ''
        samples_float = np.empty_like(input_items[0][::n_sample])

        for index in range(n_sample/2, len(input_items[0]) - 1, n_sample):
            if index >= len(samples_float):
                break
            samples_float[index]= input_items[0][index]
            samples = samples + str((input_items[0][index].astype(int)))


        if samples.find(self.preambule) != -1:
            start_preambule = samples.find(self.preambule)
            start_data = start_preambule + len(self.preambule)

            for i in range(start_data, (len(samples) - len(self.preambule))):
                if int(samples_float[i].astype(int)) >= 1:
                    output_items[0][retorno] = 1

                if int(samples_float[i].astype(int)) <= 0:
                    output_items[0][retorno] = 0
                # output_items[0][retorno] = samples_float[i]
                # print(int(samples_float[i].astype(int)))
                retorno = retorno + 1

            print(output_items[0:11])
            return retorno

        else:
            print("DEU RUIM")
            return retorno
