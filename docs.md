![network config](media/network-config.png)

Testing between two devices, no encryption on Channel 48. Channel 48 is a 1 MHz channel centered at 920.5 MHz. Even with no information moving over the network, it is fairly chatty:

![spectrum waterfall](media/spectrum-waterfall.png)

according to docs, MCS 10 is BPSK with R = 1/2 with 2x repetition. This differs from MCS 0 that is also BPSK but R = 1/2, no repetition. With a 8us guard interval, you can expect 150kbps. Going to start simple and try to implement MCS 0 to start, then I'll progress up the MCS in complexity

![mcs](media/mcs-nsss.png)

## Todo

- [ ] Range testing at this channel, propagation analysis model
- [ ] how can you determine whether there is 1 or multiple spatial streams? 
- [ ] is there a way to verify on the HaLow which MCS index is being used? It might be automatically negotiated based on what is available; will also have to read through the specification more to determine if this is the case. What worries me is that the network config picture shows that the TX and RX rate is 6 Mbps which means that the HaLow's may have negotiated for multiple spatial streams and a higher MCS. Just with a cursory look, it seems like this time domain plot is multi-level phase shift keying. For BPSK I would expect constant amplitude
![time domain](media/time-domain-halow-capture.jpg)