import numpy as np
from gnuradio import gr
import pmt
import json

class blk(gr.sync_block):  


    def __init__(self, upper_detection_threshold=0.2, halow_channel_json_filename="/home/dragon/Documents/gr-halow/flowgraphs/halow_channels.json"): 
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='HaLow Usage Detector',  
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.upper_detection_threshold = upper_detection_threshold
        self.halow_channel_json_filename = halow_channel_json_filename
        json_file = open(self.halow_channel_json_filename)
        self.all_halow_channels = json.load(json_file)
        json_file.close()
        self.port_freq_in = "freq_in"
        self.message_port_register_in(pmt.intern(self.port_freq_in))
        self.set_msg_handler(pmt.intern(self.port_freq_in), self.handle_freq_in)
        self.port_tune_in = "tune_in"
        self.message_port_register_in(pmt.intern(self.port_tune_in))
        self.set_msg_handler(pmt.intern(self.port_tune_in), self.handle_tune_in)
        self.tune_frequency = 0
        self.offset_frequency = 0

    def handle_tune_in(self, msg):
        key = pmt.intern("freq")
        value = pmt.dict_ref(msg, key, pmt.PMT_NIL) 
        if(value is not pmt.PMT_NIL):
            self.tune_frequency = pmt.to_double(value)
    
    def handle_freq_in(self, msg):
        key = pmt.intern("freq")
        value = pmt.dict_ref(msg, key, pmt.PMT_NIL) 
        if(value is not pmt.PMT_NIL):
            self.offset_frequency = pmt.to_double(value)

    def channel_lookup(self):
        channel_frequency = self.tune_frequency + self.offset_frequency
        for channel, value in self.all_halow_channels.items():
            if(value["freq"] == channel_frequency):
                return (channel, value)
        return (-1, -1)

    def work(self, input_items, output_items):
        # this block does not operate on samples
        output_items[0][:] = input_items[0]

        # find any identified wifi frames and print out the current channel
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        channel = self.channel_lookup()
        for tag in tags:
            key = pmt.to_python(tag.key)
            value = pmt.to_python(tag.value)
            if(np.abs(value) < self.upper_detection_threshold and channel[0] != -1):
                channel_freq = channel[1]["freq"]/1e6
                channel_bw   = channel[1]["bw"]/1e6
                print(f"HaLow activity - channel {channel[0]}, freq {channel_freq} MHz, bw {channel_bw} MHz - {value:.3f}")

        return len(output_items[0])
