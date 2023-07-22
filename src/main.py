from machine import Pin, SPI
from micropython import const
import struct
import ubinascii

GetVersion = const(0x30)
GetSN = const(0x32)
Import_Sym_Ke = const(0x42)
Sym_Encrypt = const(0x44)
Sym_Decrypt = const(0x46)
Sym_Duplex_Encrypt = const(0x45)
Sym_Duplex_Decrypt = const(0x47)

SM2_Gen_Key = const(0x5A)
SM2_Import_Key = const(0x5C)
SM2_Export_Key = const(0x5E)
SM2_Sign = const(0x60)
SM2_Verify = const(0x62)
SM2_Encrypt = const(0x64)
SM2_Decrypt = const(0x66)
SM2_PriKey_Gen_PubKey = const(0x68)

SM2_Import_Sym_Key = const(0x73)

Device_Authenticate = const(0x82)
Write_User_Data = const(0x80)
Read_User_Data = const(0x81)


def print_bytes_hex(data):
    lin = ['0x%02X' % i for i in data]
    print(" ".join(lin))


class SendPacket:
    def __init__(self, use_crc32, data, recv_lenth, command):
        self.pack = b''
        # header
        self.pack += struct.pack('<I', 0x33100253)

        # data_length
        self.pack += struct.pack('<I', recv_lenth)

        # command
        self.pack += command

        # reserve
        self.pack += struct.pack('I', 0x55555555)
        # data
        if data != None:
            self.pack += data

        # footer
        self.pack += struct.pack('I', 0x01330255)

        # crc32
        if use_crc32:
            self.pack += struct.pack('I', ubinascii.crc32(self.pack))

    def raw(self):
        return self.pack


class RecvPacket:
    def __init__(self, data):
        self.o = data
        self.packet_header = struct.unpack('<I', data[:4])[0]
        self.data_length = struct.unpack('<I', data[4:8])[0]
        self.status_byte = struct.unpack('<H', data[8:10])[0]
        self.reserved = struct.unpack('<6s', data[10:16])[0]
        self.data = data[16:-8]
        self.packet_footer = struct.unpack('<I', data[-8:-4])[0]
        self.crc32_checksum = struct.unpack('<I', data[-4:])[0]

    def validate_crc32(self):
        calculated_crc32 = ubinascii.crc32(self.data)
        return calculated_crc32 == self.crc32_checksum

    def get_status(self):
        return self.status_byte

    def get_data(self):
        return self.data

    def raw(self):
        return self.o


class CCM3310:
    def littlechat(self, send_buf, recv_lenth):
        pass

    def largechat(self, lenth):
        pass

    def execute(self, cla, ins, p1, p2, recv_lenth):
        cmd = self.makecmd(cla, ins, p1, p2)
        send_pack = bytes()
        if cla == 0x80:
            send_pack = SendPacket(False, None, recv_lenth, cmd).raw()
        elif cla == 0x81:
            send_pack = SendPacket(True, None, recv_lenth, cmd).raw()

        recv_pack = self.littlechat(send_pack, 100)
        print_bytes_hex(recv_pack)
        # r = RecvPacket(recv_pack)
        # print(r.raw())

    def write_data(self, cla, off, write_len, data, recv_lenth):
        cmd = self.makecmd(cla, Write_User_Data, 0x00, 0x00)
        b = struct.pack('<II', off, write_len)
        b += data
        send_pack = bytes()
        if cla == 0x80:
            send_pack = SendPacket(False, b, recv_lenth, cmd).raw()
        elif cla == 0x81:
            send_pack = SendPacket(True, b, recv_lenth, cmd).raw()

        recv_pack = self.littlechat(send_pack, len(send_pack))
        r = RecvPacket(recv_pack)

    def read_data(self, cla, off, read_len, recv_lenth):
        cmd = self.makecmd(cla, Read_User_Data, 0x00, 0x00)
        b = struct.pack('<II', off, read_len)
        send_pack = bytes()
        if cla == 0x80:
            send_pack = SendPacket(False, b, recv_lenth, cmd).raw()
        elif cla == 0x81:
            send_pack = SendPacket(True, b, recv_lenth, cmd).raw()

        recv_pack = self.littlechat(send_pack, len(send_pack))
        r = RecvPacket(recv_pack)

    def makecmd(self, cls, ins, p1, p2):
        cmd = struct.pack('BBBB', cls, ins, p1, p2)
        return cmd


class SPI_CCM3310(CCM3310):
    def __init__(self, baudrate):
        self.baudrate = baudrate
        self.CPOL = 1
        self.CPHA = 1

        self.POR = Pin(33, Pin.OUT, value=0)
        self.GINT0 = Pin(14, Pin.OUT, value=1)
        self.GINT1 = Pin(32, Pin.IN)
        self.CS = Pin(5, Pin.OUT, value=1)
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
        self.POR.on()

    def littlechat(self, send_buf, recv_lenth):
        self.CS.on()
        self.CS.off()
        self.GINT0.off()
        while self.GINT1.value() == 1:
            pass
        self.spi.write(send_buf)
        self.CS.on()

        while self.GINT1.value() == 1:
            pass
        self.CS.on()
        self.CS.off()
        recv_buf = self.spi.read(recv_lenth)
        self.CS.on()
        return recv_buf


if __name__ == "__main__":
    dev = SPI_CCM3310(1000000)
    dev.execute(0x80, 0x30, 0x00, 0x00, 80)
