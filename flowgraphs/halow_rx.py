#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Halow Rx
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import ieee802_11
import sip



class halow_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Halow Rx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Halow Rx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "halow_rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.window_size = window_size = 24
        self.sync_length = sync_length = 320
        self.stop_time = stop_time = 0.31
        self.start_time = start_time = 0.292
        self.sdr_center_freq = sdr_center_freq = 918000000
        self.num_ofdm_subcarriers = num_ofdm_subcarriers = 32
        self.lo_offset = lo_offset = 0
        self.input_samp_rate = input_samp_rate = 10e6
        self.gain = gain = 0.75
        self.freq = freq = 920.5e6
        self.filter_transition = filter_transition = 10e3
        self.filter_cutoff = filter_cutoff = (samp_rate / 2) + (samp_rate /10)
        self.chan_est = chan_est = 0
        self.additional_window_size = additional_window_size = 8

        ##################################################
        # Blocks
        ##################################################

        self._sdr_center_freq_range = Range(902000000, 928000000, 100000, 918000000, 200)
        self._sdr_center_freq_win = RangeWidget(self._sdr_center_freq_range, self.set_sdr_center_freq, "'sdr_center_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sdr_center_freq_win)
        # Create the options list
        self._samp_rate_options = [1000000.0, 2000000.0, 4000000.0, 5000000.0, 10000000.0, 20000000.0]
        # Create the labels list
        self._samp_rate_labels = ['1 MHz', '2 MHz', '4 MHz', '5 MHz', '10 MHz', '20 MHz']
        # Create the combo box
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("'samp_rate'" + ": "))
        self._samp_rate_combo_box = Qt.QComboBox()
        self._samp_rate_tool_bar.addWidget(self._samp_rate_combo_box)
        for _label in self._samp_rate_labels: self._samp_rate_combo_box.addItem(_label)
        self._samp_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._samp_rate_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._samp_rate_options.index(i)))
        self._samp_rate_callback(self.samp_rate)
        self._samp_rate_combo_box.currentIndexChanged.connect(
            lambda i: self.set_samp_rate(self._samp_rate_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._samp_rate_tool_bar)
        # Create the options list
        self._freq_options = [920500000, 921000000, 922000000, 2412000000.0, 2417000000.0, 2422000000.0, 2427000000.0, 2432000000.0, 2437000000.0, 2442000000.0, 2447000000.0, 2452000000.0, 2457000000.0, 2462000000.0, 2467000000.0, 2472000000.0, 2484000000.0, 5170000000.0, 5180000000.0, 5190000000.0, 5200000000.0, 5210000000.0, 5220000000.0, 5230000000.0, 5240000000.0, 5250000000.0, 5260000000.0, 5270000000.0, 5280000000.0, 5290000000.0, 5300000000.0, 5310000000.0, 5320000000.0, 5500000000.0, 5510000000.0, 5520000000.0, 5530000000.0, 5540000000.0, 5550000000.0, 5560000000.0, 5570000000.0, 5580000000.0, 5590000000.0, 5600000000.0, 5610000000.0, 5620000000.0, 5630000000.0, 5640000000.0, 5660000000.0, 5670000000.0, 5680000000.0, 5690000000.0, 5700000000.0, 5710000000.0, 5720000000.0, 5745000000.0, 5755000000.0, 5765000000.0, 5775000000.0, 5785000000.0, 5795000000.0, 5805000000.0, 5825000000.0, 5860000000.0, 5870000000.0, 5880000000.0, 5890000000.0, 5900000000.0, 5910000000.0, 5920000000.0]
        # Create the labels list
        self._freq_labels = ['48 | 920.5 | 11ah', '159 | 921.0 | 11ah', '165 | 922.0 | 11ah', '1 | 2412.0 | 11g', '  2 | 2417.0 | 11g', '  3 | 2422.0 | 11g', '  4 | 2427.0 | 11g', '  5 | 2432.0 | 11g', '  6 | 2437.0 | 11g', '  7 | 2442.0 | 11g', '  8 | 2447.0 | 11g', '  9 | 2452.0 | 11g', ' 10 | 2457.0 | 11g', ' 11 | 2462.0 | 11g', ' 12 | 2467.0 | 11g', ' 13 | 2472.0 | 11g', ' 14 | 2484.0 | 11g', ' 34 | 5170.0 | 11a', ' 36 | 5180.0 | 11a', ' 38 | 5190.0 | 11a', ' 40 | 5200.0 | 11a', ' 42 | 5210.0 | 11a', ' 44 | 5220.0 | 11a', ' 46 | 5230.0 | 11a', ' 48 | 5240.0 | 11a', ' 50 | 5250.0 | 11a', ' 52 | 5260.0 | 11a', ' 54 | 5270.0 | 11a', ' 56 | 5280.0 | 11a', ' 58 | 5290.0 | 11a', ' 60 | 5300.0 | 11a', ' 62 | 5310.0 | 11a', ' 64 | 5320.0 | 11a', '100 | 5500.0 | 11a', '102 | 5510.0 | 11a', '104 | 5520.0 | 11a', '106 | 5530.0 | 11a', '108 | 5540.0 | 11a', '110 | 5550.0 | 11a', '112 | 5560.0 | 11a', '114 | 5570.0 | 11a', '116 | 5580.0 | 11a', '118 | 5590.0 | 11a', '120 | 5600.0 | 11a', '122 | 5610.0 | 11a', '124 | 5620.0 | 11a', '126 | 5630.0 | 11a', '128 | 5640.0 | 11a', '132 | 5660.0 | 11a', '134 | 5670.0 | 11a', '136 | 5680.0 | 11a', '138 | 5690.0 | 11a', '140 | 5700.0 | 11a', '142 | 5710.0 | 11a', '144 | 5720.0 | 11a', '149 | 5745.0 | 11a (SRD)', '151 | 5755.0 | 11a (SRD)', '153 | 5765.0 | 11a (SRD)', '155 | 5775.0 | 11a (SRD)', '157 | 5785.0 | 11a (SRD)', '159 | 5795.0 | 11a (SRD)', '161 | 5805.0 | 11a (SRD)', '165 | 5825.0 | 11a (SRD)', '172 | 5860.0 | 11p', '174 | 5870.0 | 11p', '176 | 5880.0 | 11p', '178 | 5890.0 | 11p', '180 | 5900.0 | 11p', '182 | 5910.0 | 11p', '184 | 5920.0 | 11p']
        # Create the combo box
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("'freq'" + ": "))
        self._freq_combo_box = Qt.QComboBox()
        self._freq_tool_bar.addWidget(self._freq_combo_box)
        for _label in self._freq_labels: self._freq_combo_box.addItem(_label)
        self._freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._freq_options.index(i)))
        self._freq_callback(self.freq)
        self._freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_freq(self._freq_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._freq_tool_bar)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_c(
            (int((stop_time - start_time) * samp_rate)), #size
            samp_rate, #samp_rate
            "input signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            (int((stop_time - start_time) * samp_rate)), #size
            samp_rate, #samp_rate
            "post sync", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            (int((stop_time - start_time) * samp_rate)), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        # Create the options list
        self._lo_offset_options = [0, 6000000.0, 11000000.0]
        # Create the labels list
        self._lo_offset_labels = ['0', '6000000.0', '11000000.0']
        # Create the combo box
        self._lo_offset_tool_bar = Qt.QToolBar(self)
        self._lo_offset_tool_bar.addWidget(Qt.QLabel("'lo_offset'" + ": "))
        self._lo_offset_combo_box = Qt.QComboBox()
        self._lo_offset_tool_bar.addWidget(self._lo_offset_combo_box)
        for _label in self._lo_offset_labels: self._lo_offset_combo_box.addItem(_label)
        self._lo_offset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._lo_offset_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._lo_offset_options.index(i)))
        self._lo_offset_callback(self.lo_offset)
        self._lo_offset_combo_box.currentIndexChanged.connect(
            lambda i: self.set_lo_offset(self._lo_offset_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._lo_offset_tool_bar)
        self.ieee802_11_sync_short_0 = ieee802_11.sync_short(0.56, 2, False, True)
        self.ieee802_11_sync_long_0 = ieee802_11.sync_long(sync_length, False, True)
        self._gain_range = Range(0, 1, 0.01, 0.75, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc((int(input_samp_rate/samp_rate)), firdes.low_pass(1, input_samp_rate, filter_cutoff, filter_transition), (freq - sdr_center_freq), input_samp_rate)
        # Create the options list
        self._chan_est_options = [0, 1, 2, 3]
        # Create the labels list
        self._chan_est_labels = ['LS', 'LMS', 'Linear Comb', 'STA']
        # Create the combo box
        # Create the radio buttons
        self._chan_est_group_box = Qt.QGroupBox("'chan_est'" + ": ")
        self._chan_est_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._chan_est_button_group = variable_chooser_button_group()
        self._chan_est_group_box.setLayout(self._chan_est_box)
        for i, _label in enumerate(self._chan_est_labels):
            radio_button = Qt.QRadioButton(_label)
            self._chan_est_box.addWidget(radio_button)
            self._chan_est_button_group.addButton(radio_button, i)
        self._chan_est_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chan_est_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._chan_est_options.index(i)))
        self._chan_est_callback(self.chan_est)
        self._chan_est_button_group.buttonClicked[int].connect(
            lambda i: self.set_chan_est(self._chan_est_options[i]))
        self.top_layout.addWidget(self._chan_est_group_box)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, input_samp_rate,True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_cc(window_size, 1, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff((window_size  + additional_window_size), 1, 4000, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/irongiant/Documents/gr-halow/captures/halow-capture-1mhz-mcs0.sigmf-data', False, (int(start_time * input_samp_rate)), (int((stop_time - start_time) * input_samp_rate)))
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, additional_window_size)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, sync_length)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.ieee802_11_sync_short_0, 2))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.ieee802_11_sync_long_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.ieee802_11_sync_short_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.ieee802_11_sync_short_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_moving_average_xx_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.ieee802_11_sync_long_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.ieee802_11_sync_long_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "halow_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filter_cutoff((self.samp_rate / 2) + (self.samp_rate /10))
        self._samp_rate_callback(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
        self.blocks_moving_average_xx_0.set_length_and_scale((self.window_size  + self.additional_window_size), 1)
        self.blocks_moving_average_xx_1.set_length_and_scale(self.window_size, 1)

    def get_sync_length(self):
        return self.sync_length

    def set_sync_length(self, sync_length):
        self.sync_length = sync_length
        self.blocks_delay_0.set_dly(int(self.sync_length))

    def get_stop_time(self):
        return self.stop_time

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_sdr_center_freq(self):
        return self.sdr_center_freq

    def set_sdr_center_freq(self, sdr_center_freq):
        self.sdr_center_freq = sdr_center_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.freq - self.sdr_center_freq))

    def get_num_ofdm_subcarriers(self):
        return self.num_ofdm_subcarriers

    def set_num_ofdm_subcarriers(self, num_ofdm_subcarriers):
        self.num_ofdm_subcarriers = num_ofdm_subcarriers

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self._lo_offset_callback(self.lo_offset)

    def get_input_samp_rate(self):
        return self.input_samp_rate

    def set_input_samp_rate(self, input_samp_rate):
        self.input_samp_rate = input_samp_rate
        self.blocks_throttle_0.set_sample_rate(self.input_samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_callback(self.freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.freq - self.sdr_center_freq))

    def get_filter_transition(self):
        return self.filter_transition

    def set_filter_transition(self, filter_transition):
        self.filter_transition = filter_transition
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))

    def get_filter_cutoff(self):
        return self.filter_cutoff

    def set_filter_cutoff(self, filter_cutoff):
        self.filter_cutoff = filter_cutoff
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))

    def get_chan_est(self):
        return self.chan_est

    def set_chan_est(self, chan_est):
        self.chan_est = chan_est
        self._chan_est_callback(self.chan_est)

    def get_additional_window_size(self):
        return self.additional_window_size

    def set_additional_window_size(self, additional_window_size):
        self.additional_window_size = additional_window_size
        self.blocks_delay_0_0.set_dly(int(self.additional_window_size))
        self.blocks_moving_average_xx_0.set_length_and_scale((self.window_size  + self.additional_window_size), 1)




def main(top_block_cls=halow_rx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
