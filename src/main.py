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


SM2_Import_Sym_Key = const(0x73)

Device_Authenticate = const(0x82)
Write_User_Data = const(0x80)
Read_User_Data = const(0x81)


def print_bytes_hex(data):
    lin = ['0x%02X' % i for i in data]
    print(" ".join(lin))


class CCM3310_SendPacket:
    def __init__(self, use_crc32, command, data, data_len):
        self.pack = b''
        # header
        self.pack += struct.pack('<I', 0x33100253)

        # data_length
        self.pack += struct.pack('<I', data_len)

        # command
        self.pack += command

        # reserve
        self.pack += struct.pack('<I', 0x55555555)
        # data
        if data != None:
            self.pack += data

        # footer
        self.pack += struct.pack('<I', 0x01330255)

        # crc32
        if use_crc32:
            self.pack += struct.pack('<I', ubinascii.crc32(self.pack))

    def release(self) -> bytearray:
        return bytearray(self.pack)


class CCM3310_RecvPacket:
    def __init__(self, data):
        self.packet_header = struct.unpack('<I', data[:4])[0]
        self.data_length = struct.unpack('<I', data[4:8])[0]
        self.status_byte = struct.unpack('<H', data[8:10])[0]
        self.reserved = struct.unpack('<6s', data[10:16])[0]
        self.data = data[16:16+self.data_length]
        self.packet_footer = struct.unpack(
            '<I', data[16+self.data_length:20+self.data_length])[0]
        self.crc32_checksum = struct.unpack(
            '<I', data[20+self.data_length:24+self.data_length])[0]

    def validate_crc32(self) -> bool:
        calculated_crc32 = ubinascii.crc32(self.data)
        return calculated_crc32 == self.crc32_checksum

    def release(self) -> bytes:
        if (self.status_byte != 0x9000) or (self.packet_header != 0x33100252) or (self.packet_footer != 0x01330256):
            return bytes(0)
        return bytes(self.data)


class CCM3310:
    def littlechat(self, send_buf, recv_lenth):
        pass

    def largechat(self, lenth):
        pass

    def version(self) -> str:
        cmd = struct.pack('BBBB', 0x80, 0x30, 0x00, 0x00)
        send_pack = CCM3310_SendPacket(
            False, cmd, None, 80).release()
        recv = self.littlechat(send_pack, 100)
        return CCM3310_RecvPacket(recv).release().decode('utf-8')

    def execute(self, cla: int, ins: int, p1: int, p2: int, data: bytes, recv_lenth: int) -> bytes:
        cmd = struct.pack('BBBB', cla, ins, p1, p2)
        send_pack = bytes()
        if cla == 0x80:
            send_pack = CCM3310_SendPacket(
                False, cmd, data, len(data)).release()
        elif cla == 0x81:
            send_pack = CCM3310_SendPacket(
                True, cmd, data, len(data)).release()

        recv_pack = self.littlechat(send_pack, recv_lenth)
        return bytes(recv_pack)


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
    print(dev.version())
