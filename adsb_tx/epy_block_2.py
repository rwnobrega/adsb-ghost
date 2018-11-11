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
            in_sig=[np.int32],
            out_sig=[np.uint8]
        )
        # self.preambule = '1010000101000000'
        self.preambule = '1010000101000000'
        self.int_to_return = []
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
    def forecast(self, noutput_items, ninput_items_required):
        ninput_items_required = 2000

    def general_work(self, input_items, output_items):
        #input_items com sinais super amostrados.
        # print("INICIO")
        if len(input_items[0]) < 2000:
            # print("BUFFER SEM TAMANHO SUFICIENTE. Esperando...")
            return 0

        # print("VAI PROCESSAR")
        # print("ITEMS NO BUFFER DE ENTRADA: ", input_items[0])
        #Confirma que ha amostras o suficiente para processar
        if not self.int_to_return:
            # # print("LISTA INTEIROS VAZIA")
            n_sample = 6 #fator de superamostragem
            samples = '' #ira comportar as amostras transformadas em string
            samples_backup = np.empty_like(input_items[0][::n_sample]) #array vazio para comportar as amostras de interesse

            #loop para retirar as superamostragem, atraves do fator de superamostragem
                #1. primeiro se guarda a amostra intocada
                #2. Depois transforma a amostra em string para que possa se buscar o preambulo posteriormente
            sample_counter = 0
            for index in range(n_sample/2, len(input_items[0]) - 1, n_sample):
                if index >= len(samples_backup):
                    break
                samples_backup[sample_counter]= input_items[0][index]
                samples = samples + str((input_items[0][index]))
                sample_counter = sample_counter + 1
            # print("AMOSTRAS SEM SUPERAMOSTRAGEM: ", samples_backup)
            # print("Quantidade de amostras: ", len(samples_backup))

            ppm_array = ''
            decoded_message = ''
            retorno = 0 #ira inidicar o numero de itens a serem retornados
            # print("STRING AMOSTRAS: ", samples)
            if samples.find(self.preambule) != -1: #Confirma se eh possivel encontrar o preambulo
                # # print("ENCONTROU O PREAMBULO")
                #Pega o inicio do preambulo e aponta onde eh o inicio das informacoes
                start_preambule = samples.find(self.preambule)
                start_data = start_preambule + len(self.preambule)

                for i in range(start_data, start_data + 224):
                    ppm_array = ppm_array + str(samples_backup[i])
                    output_items[0][retorno] = samples_backup[i]
                    retorno = retorno + 1

                for index in range(0, 223, 2):

                    if ppm_array[index] == '0' and ppm_array[index + 1] == '1':
                        decoded_message = decoded_message + '0'
                    else:
                        decoded_message = decoded_message + '1'
                # print("DECODED MESSAGE", decoded_message)
                # print("TAMANHO DA DECODED MESSAGE", len(decoded_message))

                first_message = "1000110101000000011000100001110100100000000110001100011001000100010101010100000011001000101010001101100111010110"
                second_message = "1000110101000000011000100001110101011000110000111000000110011000001011111010111000100010110101100101010111111000"

                if decoded_message == first_message:
                    print("PRIMEIRO PACOTE ACHADO")

                if decoded_message == second_message:
                    print("SEGUNDO PACOTE ACHADO")

                chunks = [decoded_message[i:i+8] for i in range(0, len(decoded_message), 8)]
                list_int = [int(x, 2) for x in chunks]
                self.int_to_return = list_int
                output_items[0][0] = self.int_to_return.pop(0)
                self.consume(0, 1440)
                # print("FINAL")
                # print("\n")
                return 1

            else:
                # print("NAO ENCONTROU O PREAMBULO")
                # print("FINAL")
                # print("\n")
                self.consume(0, len(input_items[0]) - 1)
                return 0
        else:
            if self.int_to_return:
                # print("LISTA INTEIRO NAO VAZIA")
                output_items[0][0] = self.int_to_return.pop(0)
                # print("FINAL")
                # print("\n")
                return 1


        # if len(input_items[0]) < 768:
        #     return 0
        #
        # retorno = 0
        # n_sample = 6
        # samples = ''
        # samples_float = np.empty_like(input_items[0][::n_sample])
        #
        # for index in range(n_sample/2, len(input_items[0]) - 1, n_sample):
        #     if index >= len(samples_float):
        #         break
        #     samples_float[index]= input_items[0][index]
        #     samples = samples + str((input_items[0][index].astype(int)))
        #
        # if samples.find(self.preambule) != -1:
        #     start_preambule = samples.find(self.preambule)
        #     start_data = start_preambule + len(self.preambule)
        #     for i in range(start_data, start_data + 112):
        #         if int(samples_float[i].astype(int)) >= 1:
        #             output_items[0][retorno] = 1
        #
        #         else:
        #             output_items[0][retorno] = 0
        #
        #         retorno = retorno + 1
        #     print("FIM: ", samples[0:retorno])
        #     return retorno
        #
        # else:
        #     print("DEU RUIM")
        #     return retorno
