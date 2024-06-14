# gr-halow

gr-halow is a first-of-its-kind implementation of IEEE 802.11ah Wi-Fi HaLow in GNU Radio that enables researchers, developers, and hobbyists to experiment with 802.11ah-based solutions using SDRs without the need to rely on commercial hardware implementations.

**Contents**
- [What is HaLow?](#what-is-halow)
- [How Do I Use It?](#how-do-i-use-it)
- [Applications](#applications)
- [Resources](#resources)

## What is HaLow?

IEEE 802.11ah, also known as Wi-Fi HaLow, is an implementation of Wi-Fi in sub-1GHz bands. Due to its lower operating frequency than traditional Wi-Fi, Wi-Fi HaLow trades dimished data rates for longer transmission distances. This balance is favorable to internet-of-things (IoT) and other long-range applications. Read more about Wi-Fi HaLow on The Wi-Fi Alliance's website: [https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-halow](https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-halow).

You can view the IEEE Medium Access Control (MAC) and Physical Layer (PHY) specification for 802.11ah here: [https://ieeexplore.ieee.org/browse/standards/reading-room/page/viewer?id=9363693](https://ieeexplore.ieee.org/browse/standards/reading-room/page/viewer?id=9363693). It is free to access through the IEEE REading Room after creating an IEEE account. Chapter 23 specifically pertains to Sub 1GHz PHY. In case the link dies, the title of the document is "Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications." It is the December 2020 revision of the 2016 standard.

## How Do I Use It?

🚧 Under Construction 🚧

`gr-halow` is a GNU Radio Out-of-Tree Module. Read more about GNU Radio and their out-of-tree module concept here: [https://wiki.gnuradio.org/index.php?title=Creating_Python_OOT_with_gr-modtool](https://wiki.gnuradio.org/index.php?title=Creating_Python_OOT_with_gr-modtool). To install, you should have GNU Radio Version 3.10 or above

```
git clone https://github.com/irongiant33/gr-halow.git
cd gr-halow
mkdir build
cd build
cmake ..
sudo make install
sudo ldconfig
```

## Applications

Below are some example applications of `gr-halow`. See the [resources](#resources) section for some HaLow applications that other creators have demonstrated.

### Troubleshooting HaLow Network

**RX only troubleshooting is possible**

🚧 Under Construction 🚧

### Full HaLow Client

**requires TX/RX functionality for the SDR**

🚧 Under Construction 🚧

### Scanning for HaLow Networks

**requires RX functionality only**

🚧 Under Construction 🚧

## Resources

### Media

1. Ben Jeffrey on YouTube gives an overview of IEEE 802.11ah: [https://www.youtube.com/watch?v=qF0BHnmi9j8](https://www.youtube.com/watch?v=qF0BHnmi9j8)
2. Cemaxecuter on YouTube uses HaLow for various applications
	- introduction and propagation analysis [https://www.youtube.com/watch?v=Bw6cs0_R-oQ](https://www.youtube.com/watch?v=Bw6cs0_R-oQ)
	- remote control of Pluto SDR: [https://www.youtube.com/watch?v=BNC8uKlmLfw&pp=ygURY2VtYXhlY3V0ZXIgaGFsb3c%3D](https://www.youtube.com/watch?v=BNC8uKlmLfw&pp=ygURY2VtYXhlY3V0ZXIgaGFsb3c%3D)
	- 1km remote connection: [https://www.youtube.com/watch?v=QGt4kE58CEQ&t=394s&pp=ygURY2VtYXhlY3V0ZXIgaGFsb3c%3D](https://www.youtube.com/watch?v=QGt4kE58CEQ&t=394s&pp=ygURY2VtYXhlY3V0ZXIgaGFsb3c%3D)
3. Newracom (one of the HaLow fabless chip manufacturers) tests over 1000 HaLow devices at once: [https://www.youtube.com/watch?v=xd0e3nH0KzI](ttps://www.youtube.com/watch?v=xd0e3nH0KzI)
4. Morse Micro (another fabless HaLow chip manufacturer) verifies HaLow functionality over 3km: [https://www.youtube.com/watch?v=2xlUijXucoM](https://www.youtube.com/watch?v=2xlUijXucoM)

### Commercial HaLow Devices

Other devices exist on the market, but these are two that I own and can recommend

1. Teledatics XPAH: [Teledatics Documentation](https://teledatics.com/docs/)
2. Alfa HaLow-U: [https://store.rokland.com/products/alfa-network-halow-u-802-11ah-halow-usb-adapter-support-ap-client-mode](https://store.rokland.com/products/alfa-network-halow-u-802-11ah-halow-usb-adapter-support-ap-client-mode)
