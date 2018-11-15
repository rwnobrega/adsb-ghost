"""
Embedded Python Blocks:
Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import adsb_dec



class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, access_code=None, payload_length=100, threshold=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='My Correlator Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.category = ''
        self.callsign = ''
        self.position_message = ''
        self.position = ''
        self.access_code = access_code
        self.payload_length = payload_length
        self.threshold = threshold
        self.mode = 'find'

        self.set_min_output_buffer(2**16)


    def general_work(self, input_items, output_items):
        if self.mode == 'output':
            return self.general_work_output(input_items, output_items)
        elif self.mode == 'find':
            return self.general_work_find(input_items, output_items)

    def general_work_output(self, input_items, output_items):
        L_in = len(input_items[0])
        L_out = len(output_items[0])
        L_payload = self.payload_length

        if L_in < L_payload or L_out < L_payload:
            return 0

        output_items[0][:L_payload] = input_items[0][:L_payload]
        self.consume(0, L_payload)

        n_sample = 6
        samples = ''
        sample_counter = 0
        decoded_message = ''

        for index in range(n_sample/2, len(input_items[0]), n_sample):
            if input_items[0][index] > 0.5:
                samples = samples + '1'
            else:
                samples = samples + '0'

        for index in range(0, 223, 2):
            if samples[index] == '0' and samples[index + 1] == '1':
                decoded_message = decoded_message + '0'
            else:
                decoded_message = decoded_message + '1'

        # print("DECODED_MESSAGE:    ", decoded_message)


        decoded_message_hex = hex(int(decoded_message, 2))
        decoded_message_hex = decoded_message_hex[2:-1]

        type_code = adsb_dec.typecode(decoded_message_hex)

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


        self.mode = 'find'

        return L_payload

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
        # print("TAMANHO: ", len(decoded_message))
        # if decoded_message.find(message_1) != -1:
        #     print("1 PACOTE ACHADO")
        #
        # if decoded_message.find(message_2) != -1:
        #     print("2 PACOTE ACHADO")
        #
        # if decoded_message.find(message_3) != -1:
        #     print("3 PACOTE ACHADO")
        #
        # if decoded_message.find(message_4) != -1:
        #     print("4 PACOTE ACHADO")
        #
        # if decoded_message.find(message_5) != -1:
        #     print("5 PACOTE ACHADO")
        #
        # if decoded_message.find(message_6) != -1:
        #     print("6 PACOTE ACHADO")
        #
        # if decoded_message.find(message_7) != -1:
        #     print("7 PACOTE ACHADO")
        #
        # if decoded_message.find(message_8) != -1:
        #     print("8 PACOTE ACHADO")
        #
        # if decoded_message.find(message_9) != -1:
        #     print("9 PACOTE ACHADO")
        #
        # if decoded_message.find(message_10) != -1:
        #     print("10 PACOTE ACHADO")
        #
        # if decoded_message.find(message_11) != -1:
        #     print("11 PACOTE ACHADO")
        #
        # if decoded_message.find(message_12) != -1:
        #     print("12 PACOTE ACHADO")
        #
        # if decoded_message.find(message_13) != -1:
        #     print("13 PACOTE ACHADO")
        #
        # if decoded_message.find(message_14) != -1:
        #     print("14 PACOTE ACHADO")
        #
        # if decoded_message.find(message_15) != -1:
        #     print("15 PACOTE ACHADO")
        #
        # if decoded_message.find(message_16) != -1:
        #     print("16 PACOTE ACHADO")
        #
        # if decoded_message.find(message_17) != -1:
        #     print("17 PACOTE ACHADO")
        #
        # if decoded_message.find(message_18) != -1:
        #     print("18 PACOTE ACHADO")
        #
        # if decoded_message.find(message_19) != -1:
        #     print("19 PACOTE ACHADO")
        #
        # if decoded_message.find(message_20) != -1:
        #     print("20 PACOTE ACHADO")
        #
        # if decoded_message.find(message_21) != -1:
        #     print("21 PACOTE ACHADO")

        # print('Outputted {} items.'.format(L_payload))

        # output_items[0][:L_payload] = input_items[0][:L_payload]
        # self.consume(0, L_payload)
        #
        # self.mode = 'find'
        #
        # return len(decoded_message)

    def general_work_find(self, input_items, output_items):
        L_in = len(input_items[0])

        if L_in < 5000 :
            return 0

        filter = np.array(np.ones(6), dtype=np.int)

        access_code_binary = np.array([int(b) for b in self.access_code], dtype=np.int)
        access_code_binary = np.convolve(access_code_binary, filter)

        input_decoded = np.array(input_items[0] , dtype=np.float32)

        corr = np.correlate(input_decoded, access_code_binary)
        corr = corr.tolist()

        max_corr = max(corr)

        if max_corr > 96:
            match = True
        else:
            match = False

        if not match:
            self.consume(0, L_in - len(self.access_code))
        else:
            self.consume(0, len(self.access_code))
            self.mode = 'output'
            # correlation_index = corr.index(max(corr)) + 96
            # print(correlation_index)
            # final_index = correlation_index + self.payload_length
            #
            # output_index = final_index - correlation_index
            #
            # n_sample = 6
            # samples = ''
            # sample_counter = 0
            # decoded_message = ''
            #
            # velho = open("input_items.txt", "w+")
            # for input in input_items[0]:
            #     velho.write(str(input.astype(int)))
            #
            # velho.close()
            #
            #
            # for index in range(n_sample/2 , len(input_items[0][correlation_index:final_index]), n_sample):
            #     if input_items[0][correlation_index + index] > 0.5:
            #         samples = samples + '1'
            #     else:
            #         samples = samples + '0'
            #
            # for index in range(0, 223, 2):
            #     if samples[index] == '0' and samples[index + 1] == '1':
            #         decoded_message = decoded_message + '0'
            #     else:
            #         decoded_message = decoded_message + '1'
            #
            # # print("DECODED_MESSAGE:    ", decoded_message)
            #
            # decoded_message_hex = hex(int(decoded_message, 2))
            # decoded_message_hex = decoded_message_hex[2:-1]
            #
            # type_code = adsb_dec.typecode(decoded_message_hex)
            #
            # if type_code < 1 or type_code > 4:
            #     pass
            # else:
            #     self.category = adsb_dec.category(decoded_message_hex)
            #     self.callsign = adsb_dec.callsign(decoded_message_hex)
            #
            # if (9 <= type_code <= 18 and 9 <= type_code <= 18):
            #     if self.position_message:
            #         self.position = adsb_dec.airborne_position(self.position_message, decoded_message_hex, 1, 2)
            #         self.position_message = ''
            #     else:
            #         self.position_message = decoded_message_hex
            # else:
            #     pass
            #
            # print("CATEGORY: " + str(self.category) + "          CALLSIGN: " + str(self.callsign) + "          POSITION: " + str(self.position))
            #
            # output_items[0][:len(input_items[0][correlation_index:final_index])] = input_items[0][correlation_index:final_index]
            #
            # self.consume(0, len(input_items[0]))
            #
            # return len(output_items[0])


        return 0
