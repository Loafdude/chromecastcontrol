#!/usr/bin/python3
"""
    Program that handles chromecast integration, mainly with domoticz. But also implements
    a crude rest api for controlling a chromecast, and start streaming pre-defined streams.

    This can be used to create a web interface for controlling a chromecast (for example in
    angular)

    Copyright 2018: Thomas Bowman Mørch
"""
import pychromecast

CASTS = pychromecast.get_chromecasts()

if len(CASTS) == 0:
    print("No Devices Found")
    exit()
if CASTS[0].cast_type == "audio":
    AUDIO = CASTS[0]
    VIDEO = CASTS[1]
else:
    AUDIO = CASTS[1]
    VIDEO = CASTS[0]

AUDIO.wait()
VIDEO.wait()

#if __name__ == "__main__":

