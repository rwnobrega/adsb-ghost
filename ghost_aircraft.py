#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################


# imports
import json
import logging
import sys
import crc
import numpy as np
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import math

clockRate =  None
rate = 12e6
txBw = None
txAnt = "TX/RX"
txGain = None # ('LNA', 'VGA', 'AMP')
freq = 1090e9
txChan = 0
waveFreq = None

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

	#enumerate devices
	#results = SoapySDR.Device.enumerate()
	#create device instance
	#args can be user defined or from the enumeration result
	args = dict(driver="hackrf")
	try :
		sdr = SoapySDR.Device(args)
	except:
		logging.error("HarckRF não encontrado")
		exit()

	if waveFreq is None: waveFreq = rate/10


	#set clock rate first
    if clockRate is not None:
    	sdr.setMasterClockRate(clockRate)

    #set sample rate
    sdr.setSampleRate(SOAPY_SDR_TX, txChan, rate)

    #set bandwidth
    if txBw is not None: sdr.setBandwidth(SOAPY_SDR_TX, txChan, txBw)

    #set antenna
    if txAnt is not None: sdr.setAntenna(SOAPY_SDR_TX, txChan, txAnt)

    #set overall gain
    if txGain is not None: sdr.setGain(SOAPY_SDR_TX, txChan, txGain)

    #tune frontends
    if freq is not None: sdr.setFrequency(SOAPY_SDR_TX, txChan, freq)

    #create tx stream
    txStream = sdr.setupStream(SOAPY_SDR_TX, "CF32", [txChan])
    sdr.activateStream(txStream)

    phaseAcc = 0
    phaseInc = 2*math.pi*waveFreq/rate
    
    streamMTU = sdr.getStreamMTU(txStream)
    sampsCh0 = np.array([ampl]*streamMTU, np.complex64)

	

list_commands = []

sink = []

open_file(list_commands)

print list_commands


initialize_osmocon()
