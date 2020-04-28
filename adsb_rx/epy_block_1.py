"""
Embedded Python Blocks:
Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import adsb_dec



class blk(gr.basic_block):
    def __init__(self, access_code=None, payload_length=100):
        gr.basic_block.__init__(
            self,
            name='Correlator',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        self.category = ''
        self.callsign = ''
        self.position_message = ''
        self.position = ''
        self.access_code = access_code
        self.payload_length = payload_length
        self.corr = 0

        self.set_min_output_buffer(2**16)


    def general_work(self, input_items, output_items):

        L_in = len(input_items[0])

        if L_in < 10000 :
            return 0

        access_code_binary = np.array([2*int(b)-1 for b in self.access_code], dtype=np.int)

        corr = np.correlate(input_items[0], access_code_binary)

        if np.max(corr) > 90:
            corr = corr.tolist()
            begin = corr.index(max(corr)) + 96
            L_payload = self.payload_length
            samples = ''
            decoded_message = ''

            try:
                reshaped_samples = np.reshape(input_items[0][begin: begin + L_payload], (224, 6))
            except ValueError:
                print("Need more samples. Waiting... ", len(input_items[0]))
                self.consume(0, L_in)
                return 0

            reshaped_samples = reshaped_samples.sum(1)

            counter = 0
            for item in reshaped_samples:
                if item > 0:
                    output_items[0][counter] = 1.0
                    samples = samples + '1'
                else:
                    output_items[0][counter] = 0.0
                    samples = samples + '0'
                counter += 1

            for index in range(0, 223, 2):
                if samples[index] == '0' and samples[index + 1] == '1':
                    decoded_message = decoded_message + '0'
                else:
                    decoded_message = decoded_message + '1'

            decoded_message_hex = hex(int(decoded_message, 2))
            decoded_message_hex = decoded_message_hex[2:-1]

            type_code = adsb_dec.typecode(decoded_message_hex)

            if type_code < 1 or type_code > 4:
                pass
            else:
                self.category = adsb_dec.category(decoded_message_hex)
                self.callsign = adsb_dec.callsign(decoded_message_hex)

            if (9 <= type_code <= 18 and 9 <= type_code <= 18):
                if self.position_message and (self.position_message != decoded_message_hex):
                    print(adsb_dec.oe_flag(self.position_message))
                    print(adsb_dec.oe_flag(decoded_message_hex))
                    if (adsb_dec.oe_flag(self.position_message) == 0) and (adsb_dec.oe_flag(decoded_message_hex) == 1):
                        self.position = adsb_dec.position(self.position_message, decoded_message_hex, 1, 11)
                        self.position_message = ''
                    else:
                        self.position_message = ''

                else:
                    self.position_message = ''
                    self.position_message = decoded_message_hex
            else:
                pass

            print("CATEGORY: " + str(self.category) + "          CALLSIGN: " + str(self.callsign) + "          POSITION: " + str(self.position))
            self.consume(0, L_payload + len(self.access_code))
            return 224

        else:
            self.consume(0, L_in)

        return 0
