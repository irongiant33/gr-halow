#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Halow Rx
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
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
from gnuradio import soapy
import halow_rx_epy_block_0 as epy_block_0  # embedded python block
import halow_rx_epy_block_1 as epy_block_1  # embedded python block
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
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.input_samp_rate = input_samp_rate = 10e6
        self.filter_transition = filter_transition = 10e3
        self.filter_cutoff = filter_cutoff = (samp_rate / 2) - (samp_rate /10)
        self.window_size = window_size = 24
        self.training_field_size = training_field_size = 320
        self.sdr_center_freq = sdr_center_freq = 918000000
        self.lpf_taps = lpf_taps = firdes.low_pass(1, input_samp_rate, filter_cutoff, filter_transition)
        self.loiter_time = loiter_time = 0.5
        self.halow_channel_json_filename = halow_channel_json_filename = '/home/dragon/Documents/gr-halow/flowgraphs/1mhz_halow_channels.json'
        self.guard_interval_size = guard_interval_size = 8
        self.gain = gain = 3
        self.driver = driver = "airspy"
        self.correlation_threshold = correlation_threshold = 0.4
        self.activity_threshold = activity_threshold = -80

        ##################################################
        # Blocks
        ##################################################

        self._gain_range = qtgui.Range(0, 21, 1, 3, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.soapy_custom_source_0 = None
        dev = 'driver=' + driver
        stream_args = ''
        tune_args = ['']
        settings = ['']
        self.soapy_custom_source_0 = soapy.source(dev, "fc32",
                                  1, '',
                                  stream_args, tune_args, settings)
        self.soapy_custom_source_0.set_sample_rate(0, input_samp_rate)
        self.soapy_custom_source_0.set_bandwidth(0, 0)
        self.soapy_custom_source_0.set_antenna(0, 'RX')
        self.soapy_custom_source_0.set_frequency(0, sdr_center_freq)
        self.soapy_custom_source_0.set_frequency_correction(0, 0)
        self.soapy_custom_source_0.set_gain_mode(0, False)
        self.soapy_custom_source_0.set_gain(0, gain)
        self.soapy_custom_source_0.set_dc_offset_mode(0, False)
        self.soapy_custom_source_0.set_dc_offset(0, 0)
        self.soapy_custom_source_0.set_iq_balance(0, 0)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_c(
            16500, #size
            samp_rate, #samp_rate
            "post sync short", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_1_0_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_0_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_c(
            16500, #size
            samp_rate, #samp_rate
            "post sync long", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(True)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.ieee802_11_sync_short_0 = ieee802_11.sync_short(0.7, 2, False, False)
        self.ieee802_11_sync_long_0 = ieee802_11.sync_long(training_field_size, False, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc((int(input_samp_rate/samp_rate)), lpf_taps, sdr_center_freq, input_samp_rate)
        self.epy_block_1 = epy_block_1.blk(loiter_time=loiter_time, sdr_center_freq=sdr_center_freq, sdr_samp_rate=input_samp_rate, samp_rate=samp_rate, debug=True, halow_channel_json_filename=halow_channel_json_filename)
        self.epy_block_0 = epy_block_0.blk(upper_detection_threshold=activity_threshold, correlation_threshold=correlation_threshold, halow_channel_json_filename=halow_channel_json_filename)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_cc(window_size, 1, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff((window_size  + guard_interval_size), 1, 4000, 1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, training_field_size)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, guard_interval_size)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'tuning_control'), (self.epy_block_0, 'tune_in'))
        self.msg_connect((self.epy_block_1, 'freq_control'), (self.epy_block_0, 'freq_in'))
        self.msg_connect((self.epy_block_1, 'freq_control'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))
        self.msg_connect((self.epy_block_1, 'tuning_control'), (self.soapy_custom_source_0, 'cmd'))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.ieee802_11_sync_short_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.ieee802_11_sync_long_0, 1))
        self.connect((self.blocks_divide_xx_0, 0), (self.ieee802_11_sync_short_0, 2))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.ieee802_11_sync_short_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_moving_average_xx_1, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.ieee802_11_sync_long_0, 0), (self.epy_block_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.ieee802_11_sync_long_0, 0))
        self.connect((self.ieee802_11_sync_short_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))
        self.connect((self.soapy_custom_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


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
        self.set_filter_cutoff((self.samp_rate / 2) - (self.samp_rate /10))
        self.epy_block_1.samp_rate = self.samp_rate
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0_0.set_samp_rate(self.samp_rate)

    def get_input_samp_rate(self):
        return self.input_samp_rate

    def set_input_samp_rate(self, input_samp_rate):
        self.input_samp_rate = input_samp_rate
        self.set_lpf_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))
        self.epy_block_1.sdr_samp_rate = self.input_samp_rate

    def get_filter_transition(self):
        return self.filter_transition

    def set_filter_transition(self, filter_transition):
        self.filter_transition = filter_transition
        self.set_lpf_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))

    def get_filter_cutoff(self):
        return self.filter_cutoff

    def set_filter_cutoff(self, filter_cutoff):
        self.filter_cutoff = filter_cutoff
        self.set_lpf_taps(firdes.low_pass(1, self.input_samp_rate, self.filter_cutoff, self.filter_transition))

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
        self.blocks_moving_average_xx_0.set_length_and_scale((self.window_size  + self.guard_interval_size), 1)
        self.blocks_moving_average_xx_1.set_length_and_scale(self.window_size, 1)

    def get_training_field_size(self):
        return self.training_field_size

    def set_training_field_size(self, training_field_size):
        self.training_field_size = training_field_size
        self.blocks_delay_0_0_0.set_dly(int(self.training_field_size))

    def get_sdr_center_freq(self):
        return self.sdr_center_freq

    def set_sdr_center_freq(self, sdr_center_freq):
        self.sdr_center_freq = sdr_center_freq
        self.epy_block_1.sdr_center_freq = self.sdr_center_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.sdr_center_freq)
        self.soapy_custom_source_0.set_frequency(0, self.sdr_center_freq)

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lpf_taps)

    def get_loiter_time(self):
        return self.loiter_time

    def set_loiter_time(self, loiter_time):
        self.loiter_time = loiter_time

    def get_halow_channel_json_filename(self):
        return self.halow_channel_json_filename

    def set_halow_channel_json_filename(self, halow_channel_json_filename):
        self.halow_channel_json_filename = halow_channel_json_filename
        self.epy_block_0.halow_channel_json_filename = self.halow_channel_json_filename
        self.epy_block_1.halow_channel_json_filename = self.halow_channel_json_filename

    def get_guard_interval_size(self):
        return self.guard_interval_size

    def set_guard_interval_size(self, guard_interval_size):
        self.guard_interval_size = guard_interval_size
        self.blocks_delay_0_0.set_dly(int(self.guard_interval_size))
        self.blocks_moving_average_xx_0.set_length_and_scale((self.window_size  + self.guard_interval_size), 1)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_custom_source_0.set_gain(0, self.gain)

    def get_driver(self):
        return self.driver

    def set_driver(self, driver):
        self.driver = driver

    def get_correlation_threshold(self):
        return self.correlation_threshold

    def set_correlation_threshold(self, correlation_threshold):
        self.correlation_threshold = correlation_threshold
        self.epy_block_0.correlation_threshold = self.correlation_threshold

    def get_activity_threshold(self):
        return self.activity_threshold

    def set_activity_threshold(self, activity_threshold):
        self.activity_threshold = activity_threshold
        self.epy_block_0.upper_detection_threshold = self.activity_threshold




def main(top_block_cls=halow_rx, options=None):

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
