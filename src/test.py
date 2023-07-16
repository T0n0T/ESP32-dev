from machine import Pin, SPI

cs = Pin(5, Pin.OUT, value=1)
vspi = SPI(
    2,
    baudrate=1000000,
    polarity=1,
    phase=1,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(18),
    mosi=Pin(23),
    miso=Pin(19),
)
# data = bytearray([0x33, 0x10, 0x02, 0x53, 0x00, 0x00, 0x00, 0x50, 0x80,
#                  0x30, 0x00, 0x00, 0x55, 0x55, 0x55, 0x55, 0x01, 0x33, 0x02, 0x55])
data = bytearray([0x55, 0x02, 0x33, 0x01, 0x55, 0x55, 0x55, 0x55, 0x00,
                 0x00, 0x30, 0x80, 0x50, 0x00, 0x00, 0x00, 0x53, 0x02, 0x10, 0x33])
buf = bytearray(20)
cs.on()
cs.off()
vspi.write_readinto(data, buf)
cs.on()
print(buf)

