from machine import Pin, SPI


def print_bytes_hex(data):
    lin = ['0x%02X' % i for i in data]
    print(" ".join(lin))


POR = Pin(33, Pin.OUT, value=0)
GINT0 = Pin(14, Pin.OUT, value=1)
GINT1 = Pin(32, Pin.IN)
CS = Pin(5, Pin.OUT, value=1)

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
POR.on()

send_buf = bytearray([0x55, 0x02, 0x10, 0x33,
                      0x50, 0x00, 0x00, 0x00,
                      0x80, 0x30, 0x00, 0x00,
                      0x55, 0x55, 0x55, 0x55,
                      0x55, 0x02, 0x33, 0x01])
recv_buf = bytearray(100)

GINT0.off()
while GINT1.value() == 1:
    pass
CS.on()
CS.off()
vspi.write(send_buf)
CS.on()

while GINT1.value() == 1:
    pass
CS.on()
CS.off()
vspi.readinto(recv_buf)
CS.on()
print_bytes_hex(recv_buf)
