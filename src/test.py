import struct
import binascii


class RecvPacket:
    def __init__(self, data):

        self.o = data
        self.packet_header = struct.unpack('<I', data[:4])[0]
        self.data_length = struct.unpack('<I', data[4:8])[0]
        self.status_byte = struct.unpack('<H', data[8:10])[0]
        self.reserved = struct.unpack('<6s', data[10:16])[0]
        self.data = data[16:16+self.data_length]
        self.packet_footer = struct.unpack(
            '<I', data[16+self.data_length:20+self.data_length])[0]

        # self.crc32_checksum = struct.unpack(
        #     '<I', data[20+self.data_length:])[0]

    # def validate_crc32(self):
    #     calculated_crc32 = binascii.crc32(self.data)
    #     return calculated_crc32 == self.crc32_checksum

    def get_status(self):
        return self.status_byte

    def get_data(self):
        return self.data

    def raw(self):
        return self.o


if __name__ == "__main__":
    # dev = SPI_CCM3310(1000000)
    # dev.execute(0x80, 0x30, 0x00, 0x00, 80)
    data = bytearray([
        0x52, 0x02, 0x10, 0x33,
        # 数据长度
        0x50, 0x00, 0x00, 0x00,
        # 状态字
        0x00, 0x90,
        0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A,
        # 数据区
        0x43, 0x43, 0x4d, 0x33,
        0x33, 0x31, 0x30, 0x53,
        0x2d, 0x54, 0x20, 0x53,
        0x50, 0x49, 0x20, 0x41,
        0x4c, 0x47, 0x4f, 0x20,
        0x43, 0x4f, 0x53, 0x20,
        0x56, 0x31, 0x2e, 0x33,
        0x30, 0x20, 0x32, 0x30,
        0x31, 0x39, 0x2e, 0x31,
        0x31, 0x2e, 0x32, 0x36,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x43, 0x43, 0x4d, 0x33,
        0x33, 0x31, 0x30, 0x53,
        0x2d, 0x54, 0x20, 0x51,
        0x46, 0x4e, 0x33, 0x32,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        # 包尾
        0x56, 0x02, 0x33, 0x01
    ])
    r = RecvPacket(data)
    # b = bytearray(r.status_byte)

    # if r.status_byte == 0x9000 and r.packet_header == 0x33100252:
    #     print(bytes(r.data).decode('utf-8'))

    c = 'hello 小明'
    d = c.encode('utf-8')
    print(d.hex(), type(d))
    print(d.decode('utf-8'))
