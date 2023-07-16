#
# Copyright (c) 2006-2019, RT-Thread Development Team
#
# SPDX-License-Identifier: MIT License
#
# Change Logs:
# Date           Author       Notes
# 2019-06-13     SummerGift   first version
#

import time
import network
from machine import Pin, SPI
import ubinascii
import struct

tt = struct.pack('<n', 0x33, 0x10, 0x02, 0x53)
PIN_CLK = 26  # PA3
PIN_MOSI = 27  # PA4
PIN_MISO = 28  # PA5
PIN_CS = 5

def spi_test():
    cs = Pin(5, Pin.OUT)

    spi = SPI(
        2,
        baudrate=80000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=0,
        sck=Pin(18),
        mosi=Pin(23),
        miso=Pin(19),
    )
    print(spi)

    header = bytearray([0x33, 0x10, 0x02, 0x53])
    length = bytearray([0x00, 0x00, 0x00, 0x50])
    cla = bytearray([0x80])
    ins = bytearray([0x30])
    p1 = bytearray([0x00])
    p2 = bytearray([0x00])
    reserved = bytearray([0x55, 0x55, 0x55, 0x55])
    footer = bytearray([0x01, 0x33, 0x02, 0x55])

    # Concatenate all the fields except CRC32
    byte_array = header + length + cla + ins + p1 + p2 + reserved + footer

    # Calculate CRC32
    crc32_value = ubinascii.crc32(byte_array) & 0xFFFFFFFF
    crc32 = bytearray(
        [
            crc32_value >> 24,
            (crc32_value >> 16) & 0xFF,
            (crc32_value >> 8) & 0xFF,
            crc32_value & 0xFF,
        ]
    )

    # Replace CRC32 in the byte array
    byte_array[-4:] = crc32
    buf = bytearray(20)

    cs.off()
    spi.write_readinto(byte_array, buf)
    cs.on()
    string = buf.decode('utf-8')
    print(string)


def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)

    print("Begin to connect wifi...")
    wlan.connect(ssid, password)

    if wlan.isconnected():
        print("Wifi connect successful, waitting to get IP...")
    else:
        print("Wifi connect failed.")


def main():
    ssid = "APX"
    password = "12345678"
    spi_test()
    # wifi_connect(ssid, password)


if __name__ == "__main__":
    main()
