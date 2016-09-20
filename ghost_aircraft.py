#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################


# imports
import json
import logging
import osmosdr
import sys
import crc




#Function to load json objects from strings
def open_json(line):
    try:
        return json.loads(line.strip())
    except:
        logging.warning("Not possible parse object json : " + line)
        return	""


def open_file(List):
	if len(sys.argv) < 1:
		logging.error("Arquivo não passado como parametro")
		exit()

	try:
		arquivo = sys.argv[1]
	except:
		logging.error("Erro ao abrir o arquivo")
		exit()

#Try to open the file in the event error exit the program
	try:
		arq = open(arquivo)
	except:
		logging.error("Arquivo não encontrado")
		exit()
        
#Call the function which read the file and mount a list with json objects       
	for line in arq:
		ret = open_json(line)
		if ret != "":
			List.append(ret)


#Create crc about data that is transmitted
def calc_crc(data):
	aux = crc.crc(data)
	l_crc = chr(aux&0xFF)
	h_crc = chr(aux>>8)
	return (data+h_crc+l_crc)
	#Não precisa ser usado assim, deixei assim só para exemplificar o uso do CRC.


def initialize_osmocon():

	global sink 
	sink = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
	sink.set_sample_rate(12e6)
	sink.set_center_freq(1090e6 - 10e3, 0)
	sink.set_freq_corr(0, 0)
	sink.set_gain(10, 0)
	sink.set_if_gain(20, 0)
	sink.set_bb_gain(20, 0)
	sink.set_antenna("", 0)
	sink.set_bandwidth(0, 0)

list_commands = []

sink = []

open_file(list_commands)


initialize_osmocon()
