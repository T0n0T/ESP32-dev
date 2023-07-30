from machine import Pin, SPI

def print_bytes_hex(data):
	lin = ['0x%02X' % i for i in data]
	print(" ".join(lin))


# POR = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0)
GINT0 = Pin(Pin.GPIO18, Pin.OUT, Pin.PULL_DISABLE, 1)
GINT1 = Pin(Pin.GPIO20, Pin.IN)

vspi = SPI(0, 3, 4)
# POR.write(1)


def test():
	send_buf = bytearray([0x53, 0x02, 0x10, 0x33,
						0x50, 0x00, 0x00, 0x00,
						0x80, 0x30, 0x00, 0x00,
						0x55, 0x55, 0x55, 0x55,
						0x55, 0x02, 0x33, 0x01])
	recv_buf = bytearray(100)

	GINT0.write(0)
	while GINT1.read() == 1:
		pass

	vspi.write(send_buf,20)
	while GINT1.read() == 1:
		pass

	vspi.read(recv_buf,100)
	GINT0.write(1)
	print_bytes_hex(recv_buf)
