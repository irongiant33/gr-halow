import numpy as np
from gnuradio import gr
import pmt
import json
import time

LOITER_TIME = 0.1 # in seconds

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block


    def __init__(self, center_freq=902e6, samp_rate=10e6, halow_channel_json_filename="/home/dragon/Documents/gr-halow/flowgraphs/halow_channels.json"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='HaLow Scan Control',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.halow_channel_json_filename = halow_channel_json_filename
        json_file = open(self.halow_channel_json_filename)
        self.center_freq = center_freq
        self.samp_rate = samp_rate
        self.all_halow_channels = json.load(json_file)
        self.port_freq_control = "freq_control"
        self.port_tuning_control = "tuning_control"
        self.message_port_register_out(pmt.intern(self.port_freq_control))
        self.message_port_register_out(pmt.intern(self.port_tuning_control))
        json_file.close()
        self.available_halow_channels = []
        self.channel_index = 0
        self.loiter_samples = int(LOITER_TIME * samp_rate) # how many samples to read before switching channels
        self.sample_count = 0
        self.start_time = time.time()
        
        self.find_available_channels()


    def find_available_channels(self):
        self.available_halow_channels = []
        for channel, value in self.all_halow_channels.items():
            channel_lowerbound = value["freq"] + value["bw"]/2
            channel_upperbound = value["freq"] + value["bw"]/2
            radio_lowerbound = self.center_freq - self.samp_rate / 2
            radio_upperbound = self.center_freq + self.samp_rate / 2
            if(channel_lowerbound > radio_lowerbound and channel_upperbound < radio_upperbound):
                self.available_halow_channels.append((channel, value))


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0]

        self.sample_count = self.sample_count + len(input_items[0])
        if(start_time - time.time() > LOITER_TIME):
            print("changing channels...")
            self.sample_count = 0
            self.channel_index = self.channel_index + 1
            if(self.channel_index >= len(self.available_halow_channels)):
                self.channel_index = 0

        freq_offset = 0
        if(len(self.available_halow_channels) > 0):
            freq_offset = self.available_halow_channels[self.channel_index][1]["freq"] - self.center_freq
        freq_message = pmt.make_dict()
        freq_message = pmt.dict_add(freq_message, pmt.intern("freq"), pmt.from_double(freq_offset))
        self.message_port_pub(pmt.intern(self.port_freq_control), freq_message)

        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        if(len(tags) > 0):
            channel_number = self.available_halow_channels[self.channel_index][0]
            freq = self.available_halow_channels[self.channel_index][1]["freq"]
            bw = self.available_halow_channels[self.channel_index][1]["bw"]
            print(f"HaLow active on channel {channel_number}, frequency: {freq}, bandwidth: {bw}")
            print(f"{self.sample_count} {self.loiter_samples}")

        return len(output_items[0])
