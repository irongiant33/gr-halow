![network config](media/network-config.png)

Testing between two devices, no encryption on Channel 48. Channel 48 is a 1 MHz channel centered at 920.5 MHz. Even with no information moving over the network, it is fairly chatty:

![spectrum waterfall](media/spectrum-waterfall.png)

according to docs, MCS 10 is BPSK with R = 1/2 with 2x repetition. This differs from MCS 0 that is also BPSK but R = 1/2, no repetition. With a 8us guard interval, you can expect 150kbps. Going to start simple and try to implement MCS 0 to start, then I'll progress up the MCS in complexity

![mcs](media/mcs-nsss.png)

based off of the `halow-capture.sigmf-data` looking at the symbol crossings (or what I'm guessing are the symbol crossings) on the time sink, I think the sps is somewhere between 16 and 20 which would be a 500kbaud or 650kbaud signal.

## view and modify MCS on HaLow

To view MCS:

```
ip a # ensure HaLow is booted, you should have an IP address. If not booted, serial in and enter `boot` command
sudo tio -b 115200 /dev/ttyACM0  # or whatever port the halow is connected to
cd /usr/bin
cli_app
show_config
```

![mcs config](media/mcs-config.png)

To change MCS (assuming you are already serialled into HaLowU after viewing the MCS above):

```
set rc off # turns rate control off; otherwise HaLow will negotiate best MCS for the link
test mcs 0 # enables MCS 0. Replace 0 with desired MCS, valid range is 0 to 10, inclusive
show config # verify mcs is set.
```

## testing link speed

`iperf3` is already compiled on the HaLow-U. To use:

On the server:

```
ip a # ensure you have an IP from the HaLow U, if not, enter the `boot` command after serialling in
sudo tio -b 115200 /dev/ttyACM0 # or whatever port your HaLow is connected to
cd /usr/bin
iperf3 -s -p 4444
```

On the client: **remember to enter the IP of the HaLowU, not the client!**

```
ip a # ensure you have an IP from the HaLow U, if not, enter the `boot` command after serialling in
sudo tio -b 115200 /dev/ttyACM0 # or whatever port your HaLow is connected to
cd /usr/bin
iperf3 -c 192.168.100.2 -p 4444 # or whatever the IP address of the HaLow-U node is
```

Example iperf test for MCS0

![iperf](media/iperf.png)

**must repeat this process on every device in your network**

## Misc Resources

- Wi-Fi HaLow breakdown and performance results by Troy Martin (MARCH 2024): [https://youtu.be/oFVj1RES9TU?si=XjW0Y5oUUU09URXw](https://youtu.be/oFVj1RES9TU?si=XjW0Y5oUUU09URXw)
- MCS and Data Rate Table for WiFi Standards [https://mcsindex.net/](https://mcsindex.net/)

## Todo

- [ ] Range testing at this channel, propagation analysis model. While you are range testing, see if you can force the lowest number of spatial streams and the lowest MCS.
- [x] try adding attenuators to HaLow-U to force lower MCS? **answer**: don't need to do this because you can manually set the MCS on client and server. See [view and modify MCS on HaLow](#view-and-modify-mcs-on-halow)
- [x] how can you determine whether there is 1 or multiple spatial streams? **answer**: I am fairly certain there can only be 1 spatial stream on the HaLowU because there is only 1 antenna. These explanations helped my understanding: [https://www.digitalairwireless.com/articles/blog/wi-fi-spatial-streaming-explained](https://www.digitalairwireless.com/articles/blog/wi-fi-spatial-streaming-explained). Also, the definition of a spatial stream in the HaLow specification document is "spatial stream: One of several streams of bits or modulation symbols that might be transmitted over multiple spatial dimensions that are created by the use of multiple antennas at both ends of a communications link." (p.170).
- [x] is there a way to verify on the HaLow which MCS index is being used? It might be automatically negotiated based on what is available; will also have to read through the specification more to determine if this is the case. What worries me is that the network config picture shows that the TX and RX rate is 6 Mbps which means that the HaLow's may have negotiated for multiple spatial streams and a higher MCS. Just with a cursory look, it seems like this time domain plot is multi-level phase shift keying. For BPSK I would expect constant amplitude
![time domain](media/time-domain-halow-capture.jpg)
    - "MCS Negotiation Support - Indicates if the STA supports control response MCS negotiation feature. Set to 0 if not supported. Set to 1 if supported." p.1345 of the specification within the "9.4.2.200.2 S1G Capabilities Information field" section
    - section "9.4.2.200.3 Supported S1G-MCS and NSS Set field" does the following: "convey the combinations of S1G-MCSs and spatial streams that a STA supports for reception and the combinations that it supports for transmission" p.1346. Its unclear where this is advertised & I'm not sure how to contorl this with HaLow-U, but it is possible that this is what is happening without my knowledge. In general, section 9 covers the frame formats so this is after modulation.
    - **answer**: Yes, see [view and modify MCS on HaLow](#view-and-modify-mcs-on-halow)
- [x] how many spatial streams does the Halow-U support? **answer** 4, see [mcs picture](media/mcs-nsss.png)
    - according to HaLow-U docs, it only supports 1/2/4 MHz channels, so you don't have to worry about 8 or 16 MHz channels from the IEEE specification. See specification of HaLow-U here: [https://store.rokland.com/products/alfa-network-halow-u-802-11ah-halow-usb-adapter-support-ap-client-mode](https://store.rokland.com/products/alfa-network-halow-u-802-11ah-halow-usb-adapter-support-ap-client-mode)
- [x] Attempt Wireshark FIFO to see if it detects Wi-Fi frames? **answer**: this won't be possible until there is a program that processes HaLow frames from the PHY. The reason why some people can do this with bluetooth or wifi is that there are decoders (like ice9 bluetooth sniffer) that parse raw RF into layer 2 that Wireshark can read.
    - [ ] if you have the HaLowU plugged in, does it appear as a Wireshark capture device?
- [ ] start building modem examples for a basic chatroom style tx/rx so you can lean on these for your halow tx/halow rx
- [ ] analyze the BPSK capture
- [ ] how to determine SPS? since the web app told me that I should expect 1 Mbps, can you use this information in tandem with the modulation scheme to determine SPS? For example, 6 Mbps with 16QAM should yield 1.5M baud? If this is true, maybe my timing estimates are off. Even 6 Mbps with 64 QAM would yield 1M baud and I'm seeing half that rate still.
- [ ] been 6 years since this was contributed to, but does it work? [https://github.com/dverhaert/GNUradio-802.11ah](https://github.com/dverhaert/GNUradio-802.11ah)
- [ ] any documents from newracom, morse micro that might help?
- [ ] break out gr-ieee80211 to see if you can get anything to make sense. It might not work end-to-end, but it could serve as a good basis.
- [ ] build energy detector and correlator that could identify active HaLow channels?

