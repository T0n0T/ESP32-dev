from device import CCM3310
from machine import Pin, SPI


class SPI_CCM3310(CCM3310):
    def __init__(self, baudrate):
        self.baudrate = baudrate
        self.CPOL = 1
        self.CPHA = 1
        self.cs = Pin(5, Pin.OUT_PP, value=1)
        self.spi = SPI(
            2,
            baudrate=self.baudrate,
            polarity=self.CPOL,
            phase=self.CPHA,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(18),
            mosi=Pin(23),
            miso=Pin(19),
        )

    def wirte(self, data):
        self.cs.on()
        self.cs.off()
        self.spi.write(bytearray([data]))
        self.cs.on()

    def read(self, buf):
        self.cs.on()
        self.cs.off()
        self.spi.readinto(buf=bytearray([buf]))
        self.cs.on()

    def write2read(self, data, buf):
        self.cs.on()
        self.cs.off()
        self.spi.write_readinto(bytearray([data]), bytearray([buf]))
        self.cs.on()
