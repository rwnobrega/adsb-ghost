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
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Decoder',
            in_sig=[np.uint32],
            out_sig=[np.uint8]
        )
        self.preambule = '1010000101000000'
        self.int_to_return = []
        self.leftover = ''
        self.position_message = ''

        self.callsign = ''
        self.category = ''
        self.position = ''

    def forecast(self, noutput_items, ninput_items_required):
        ninput_items_required = 2000

    def general_work(self, input_items, output_items):

        if len(input_items[0]) < 2000:
            return 0


        if not self.int_to_return:
            n_sample = 6
            samples = ''

            sample_counter = 0
            for index in range(n_sample/2, len(input_items[0]) - 1, n_sample):
            # ~for index in range(0, len(input_items[0]) - 1):

                samples = samples + str((input_items[0][index]))
                sample_counter = sample_counter + 1


            samples = self.leftover + samples


            ppm_array = ''
            decoded_message = ''
            if samples.find(self.preambule) != -1:

                start_preambule = samples.find(self.preambule)
                start_data = start_preambule + len(self.preambule)

                for i in range(start_data, start_data + 224):
                    ppm_array = ppm_array + samples[i]

                for index in range(0, 223, 2):
                    if ppm_array[index] == '0' and ppm_array[index + 1] == '1':
                        decoded_message = decoded_message + '0'
                    else:
                        decoded_message = decoded_message + '1'

                self.leftover = samples[0:start_preambule] + samples[start_data:]


                # message_1 = "1000110101000000011000100001110100100000000110001100011001000100010101010100000011001000101010001101100111010110"
                # message_2 = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"
                # message_3 = "1000110101000000011000100001110101011000110000111000010111100110101110111111001101001111011001010001000011010000"
                # message_4 = "1000110101000000011000100001110101011000110000111000001111111001101010010111110011110100001111110000010010010111"
                # message_5 = "1000110101000000011000100001110101011000110000111000010001001111000111011100010111001110111011011101100000100110"
                # message_6 = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"
                # message_7 = "1000110101000000011000100001110101011000110000111000010111100110101110111111001101001111011001010001000011010000"
                # message_8 = "1000110101000000011000100001110101011000110000111000001000101111001010111010101000010111110011110001100001010011"
                # message_9 = "1000110101000000011000100001110101011000110000111000011010011101010101011011011100011000101000110101011111110011"
                # message_10 = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"
                # message_11 = "1000110101000000011000100001110101011000110000111000010111100110101110111111001101001111011001010001000011010000"
                # message_12 = "1000110101000000011000100001110101011000110000111000001100000011101110001010111001011011010110010101111001011011"
                # message_13 = "1000110101000000011000100001110101011000110000111000011001101110010101101001101101001100011111010111101111100110"
                # message_14 = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"
                # message_15 = "1000110101000000011000100001110101011000110000111000010111100110101110111111001101001111011001010001000011010000"
                # message_16 = "1000110101000000011000100001110101011000110000111000001011101010010101101111101011010100100101000111011100011010"
                # message_17 = "1000110101000000011000100001110101011000110000111000011001010101011000101111001111011110000001001111111011010011"
                # message_18 = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"
                # message_19 = "1000110101000000011000100001110101011000110000111000010111100110101110111111001101001111011001010001000011010000"
                # message_20 = "1000110101000000011000100001110101011000110000111000000110001101100110111011010010110011110111000100010001001101"
                # message_21 = "1000110101000000011000100001110101011000110000111000010111011100010100111111100111000000011100101010100011000101"
                #
                #
                #
                # if decoded_message == message_1:
                #     print("1 PACOTE ACHADO")
                #
                # if decoded_message == message_2:
                #     print("2 PACOTE ACHADO")
                #
                # if decoded_message == message_3:
                #     print("3 PACOTE ACHADO")
                #
                # if decoded_message == message_4:
                #     print("4 PACOTE ACHADO")
                #
                # if decoded_message == message_5:
                #     print("5 PACOTE ACHADO")
                #
                # if decoded_message == message_6:
                #     print("6 PACOTE ACHADO")
                #
                # if decoded_message == message_7:
                #     print("7 PACOTE ACHADO")
                #
                # if decoded_message == message_8:
                #     print("8 PACOTE ACHADO")
                #
                # if decoded_message == message_9:
                #     print("9 PACOTE ACHADO")
                #
                # if decoded_message == message_10:
                #     print("10 PACOTE ACHADO")
                #
                # if decoded_message == message_11:
                #     print("11 PACOTE ACHADO")
                #
                # if decoded_message == message_12:
                #     print("12 PACOTE ACHADO")
                #
                # if decoded_message == message_13:
                #     print("13 PACOTE ACHADO")
                #
                # if decoded_message == message_14:
                #     print("14 PACOTE ACHADO")
                #
                # if decoded_message == message_15:
                #     print("15 PACOTE ACHADO")
                #
                # if decoded_message == message_16:
                #     print("16 PACOTE ACHADO")
                #
                # if decoded_message == message_17:
                #     print("17 PACOTE ACHADO")
                #
                # if decoded_message == message_18:
                #     print("18 PACOTE ACHADO")
                #
                # if decoded_message == message_19:
                #     print("19 PACOTE ACHADO")
                #
                # if decoded_message == message_20:
                #     print("20 PACOTE ACHADO")
                #
                # if decoded_message == message_21:
                #     print("21 PACOTE ACHADO")


                decoded_message_hex = hex(int(decoded_message, 2))
                decoded_message_hex = decoded_message_hex[2:-1]

                type_code = adsb_dec.typecode(decoded_message_hex)



                # print("TYPE CODE: ", type_code)
                # print("TAMANHO PACOTE: ", decoded_message_hex)

                if type_code < 1 or type_code > 4:
                    pass
                else:
                    self.category = adsb_dec.category(decoded_message_hex)
                    self.callsign = adsb_dec.callsign(decoded_message_hex)

                if (9 <= type_code <= 18 and 9 <= type_code <= 18):
                    if self.position_message:
                        self.position = adsb_dec.airborne_position(self.position_message, decoded_message_hex, 1, 2)
                        self.position_message = ''
                    else:
                        self.position_message = decoded_message_hex
                else:
                    pass

                print("CATEGORY: " + str(self.category) + "          CALLSIGN: " + str(self.callsign) + "          POSITION: " + str(self.position))
                chunks = [decoded_message[i:i+8] for i in range(0, len(decoded_message), 8)]
                list_int = [int(x, 2) for x in chunks]
                self.int_to_return = list_int
                output_items[0][0] = self.int_to_return.pop(0)




                self.consume(0, len(input_items[0]))
                return 1

            else:
                self.leftover = samples

                self.consume(0, len(input_items[0]))
                return 0
        else:
            if self.int_to_return:
                output_items[0][0] = self.int_to_return.pop(0)
                return 1
