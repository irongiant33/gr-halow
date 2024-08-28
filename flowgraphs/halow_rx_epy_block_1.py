import numpy as np
from gnuradio import gr
import pmt
import json
import os

class blk(gr.sync_block): 
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, loiter_time=2, sdr_center_freq=902e6, sdr_samp_rate=10e6, samp_rate=1e6, halow_channel_json_filename=""):
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='HaLow Scan Controller', 
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.halow_channel_json_filename = halow_channel_json_filename
        self.all_halow_channels = {}
        if(os.path.isfile(halow_channel_json_filename)):
            json_file = open(self.halow_channel_json_filename)
            self.all_halow_channels = json.load(json_file)
            json_file.close()
        self.sdr_center_freq = sdr_center_freq
        self.samp_rate = samp_rate
        self.sdr_samp_rate = sdr_samp_rate
        self.port_freq_control = "freq_control"
        self.port_tuning_control = "tuning_control"
        self.message_port_register_out(pmt.intern(self.port_freq_control))
        self.message_port_register_out(pmt.intern(self.port_tuning_control))
        self.available_halow_channels = []
        self.channel_index = 0
        self.loiter_samples = int(loiter_time * samp_rate) # how many samples to read before switching channels
        self.sample_count = 0
        self.freq_message = None
        self.tune_message = None

        # first time setup operations
        self.find_available_channels()
        freq_offset = 0 # initial offset of 0 unless there are available channels
        if(len(self.available_halow_channels) > 0):
            freq_offset = self.available_halow_channels[self.channel_index][1]["freq"] - self.sdr_center_freq
        self.set_freq_message(freq_offset) # initial offset of 0

    def find_available_channels(self):
        self.available_halow_channels = []
        for channel, value in self.all_halow_channels.items():
            channel_lowerbound = value["freq"] - value["bw"]/2
            channel_upperbound = value["freq"] + value["bw"]/2
            radio_lowerbound = self.sdr_center_freq - self.sdr_samp_rate / 2
            radio_upperbound = self.sdr_center_freq + self.sdr_samp_rate / 2
            if(channel_lowerbound >= radio_lowerbound and channel_upperbound <= radio_upperbound):
                self.available_halow_channels.append((channel, value))

    def find_next_tuning_freq(self):
        radio_lowerbound = self.sdr_center_freq - self.sdr_samp_rate / 2
        radio_upperbound = self.sdr_center_freq + self.sdr_samp_rate / 2
        search_lowerbound = radio_upperbound - 4e6 # 4e6 because it is the maximum width of a HaLow channel that we care about
        first_channel_miss = None # we will set the radio lowerbound so that it captures the first missed channel
        count = 0 # ensures we don't have endless while loop
        if(search_lowerbound < radio_lowerbound):
            search_lowerbound = radio_lowerbound

        # find first channel miss
        while(first_channel_miss is None):
            for channel, value in self.all_halow_channels.items():
                # detect miss
                right_of_search_lowerbound = value["freq"] >= search_lowerbound
                outside_current_range      = radio_upperbound < (value["freq"] + value["bw"]/2)
                sdr_can_capture            = value["bw"] <= self.sdr_samp_rate
                if(right_of_search_lowerbound and outside_current_range and sdr_can_capture):
                    # new lowest miss
                    if(first_channel_miss is None or value["freq"] < first_channel_miss[1]["freq"]):
                        first_channel_miss = (channel, value)
            # wraparound condition
            if(first_channel_miss is None and count < 1):
                search_lowerbound = 902e6 # lowest edge of ISM band
                radio_upperbound = 901e6 # 1MHz lower than lowest edge of ISM band
                count = count + 1
            elif(first_channel_miss is None and count >= 1):
                return self.sdr_center_freq
        
        new_tuning_freq = (self.sdr_samp_rate / 2) + (first_channel_miss[1]["freq"] - first_channel_miss[1]["bw"] / 2)
        return new_tuning_freq


    def set_freq_message(self, freq_offset):
        self.freq_message = pmt.make_dict()
        self.freq_message = pmt.dict_add(self.freq_message, pmt.intern("freq"), pmt.from_double(freq_offset))

    def set_tune_message(self, tuning_freq):
        self.sdr_center_freq = tuning_freq
        self.tune_message = pmt.make_dict()
        self.tune_message = pmt.dict_add(self.tune_message, pmt.intern("freq"), pmt.from_double(tuning_freq))
        self.find_available_channels()

    def work(self, input_items, output_items):
        # pass all samples through; this block doesn't change samples, it just detects them for timing
        output_items[0][:] = input_items[0]

        # increment sample count so we know how long we've stared at a channel before switching to the next
        self.sample_count = self.sample_count + len(input_items[0])
        if(self.sample_count > self.loiter_samples):
            self.sample_count = 0
            self.channel_index = self.channel_index + 1
            # check for rollover condition
            if(self.channel_index >= len(self.available_halow_channels)):
                self.channel_index = 0
                next_tuning_freq = self.find_next_tuning_freq()
                self.set_tune_message(next_tuning_freq)
            if(len(self.available_halow_channels) > 0):
                self.set_freq_message(self.available_halow_channels[self.channel_index][1]["freq"] - self.sdr_center_freq)

        # control FIR filter and tuner
        self.message_port_pub(pmt.intern(self.port_freq_control), self.freq_message)
        self.message_port_pub(pmt.intern(self.port_tuning_control), self.tune_message)
        
        # GRC expects this as a return value
        return len(output_items[0])

