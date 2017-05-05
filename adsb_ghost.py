#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Adsb Ghost
# Generated: Wed May  3 15:55:31 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy as np
import osmosdr
import ppm_mapper
import sip
import sys
from gnuradio import qtgui


class adsb_ghost(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Adsb Ghost")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Adsb Ghost")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "adsb_ghost")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 12e6
        self.Rs = Rs = 2e6
        self.sps = sps = int(samp_rate / Rs)
        self.preamble = preamble = 0xA140
        self.freq_corr = freq_corr = 0
        self.fc = fc = 1090e6
        self.adsb_data = adsb_data = 0x8D4840D6205054D414631992CFCF

        ##################################################
        # Blocks
        ##################################################
        self._freq_corr_range = Range(-100, 100, 0.5, 0, 200)
        self._freq_corr_win = RangeWidget(self._freq_corr_range, self.set_freq_corr, "freq_corr", "counter_slider", float)
        self.top_layout.addWidget(self._freq_corr_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.ppm_mapper = ppm_mapper.blk()
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(fc - 10e3, 0)
        self.osmosdr_sink_0.set_freq_corr(freq_corr, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(30, 0)
        self.osmosdr_sink_0.set_bb_gain(30, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, (np.ones(sps)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_i(tuple(int(x) for x in bin(preamble)[2:]), True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_i(tuple(int(x) for x in bin(adsb_data)[2:]), True, 1, [])
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_int*1, (16, 2*112, 1000000))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10e3, 1, 0)
        self.analog_const_source_x_0 = analog.sig_source_i(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_mux_0, 2))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_int_to_float_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.ppm_mapper, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.ppm_mapper, 0), (self.blocks_stream_mux_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "adsb_ghost")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate / self.Rs))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_Rs(self):
        return self.Rs

    def set_Rs(self, Rs):
        self.Rs = Rs
        self.set_sps(int(self.samp_rate / self.Rs))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.interp_fir_filter_xxx_0.set_taps((np.ones(self.sps)))

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_vector_source_x_0_0.set_data(tuple(int(x) for x in bin(self.preamble)[2:]), [])

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.osmosdr_sink_0.set_freq_corr(self.freq_corr, 0)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.osmosdr_sink_0.set_center_freq(self.fc - 10e3, 0)

    def get_adsb_data(self):
        return self.adsb_data

    def set_adsb_data(self, adsb_data):
        self.adsb_data = adsb_data
        self.blocks_vector_source_x_0.set_data(tuple(int(x) for x in bin(self.adsb_data)[2:]), [])


def main(top_block_cls=adsb_ghost, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
