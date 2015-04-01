import struct
import binascii

__all__ = ('SRecordType', 'SRecord')

from enum import Enum
from colored import fore, back, style
from zwuenf.pysrec import SRecordParsingError


class SRecordType(Enum):
    HEADER = 0
    DATA = 1
    COUNT = 2
    TERMINATION = 3
    UNKNOWN = 4


class SRecord:
    """Data srtructure fot holding SRecords"""

    MIN_RECORD_LEN = 10
    DEFAULT_ADDR_LEN = 6

    # address length in bytes for all record types
    ADDR_LEN = {
        0: 2,
        1: 2,
        2: 3,
        3: 4,
        5: 2,
        7: 4,
        8: 3,
        9: 2
    }

    def __init__(self, str):
        """SRecord constructor"""

        self.type = 0x00
        self.count = 0x00
        self.address = 0x00
        self.data = list()
        self.crc = 0x00

        self.__parse__(str)

    def __parse__(self, rec):
        """Parse SRecord from string"""

        rec = rec.strip('\r\n')

        if len(rec) % 2 != 0:
            raise SRecordParsingError

        if len(rec) <= SRecord.MIN_RECORD_LEN:
            raise SRecordParsingError

        str_type = rec[0:2]
        str_count = rec[2:4]

        self.type = int(str_type[1], 16)
        self.count = int(str_count, 16)

        str_addr = rec[4:4 + self.address_len()]
        str_data = rec[4 + self.address_len():-2]
        str_crc = rec[-2:]

        # not all records used to have a address field entry
        self.address = None
        if len(str_addr) > 0:
            self.address = int(str_addr, 16)

        # not all records used to have a data field entry
        self.data = None
        if len(str_data) > 0:
            self.data = [int(str_data[i:i + 2], 16) for i in range(len(str_data))[::2]]

        self.crc = int(str_crc, 16)

    def address_len(self):
        """Get address length in bytes for the S-Record"""

        if self.record_group() is SRecordType.UNKNOWN:
            return self.DEFAULT_ADDR_LEN
        else:
            return SRecord.ADDR_LEN[self.type]

    def record_group(self):
        """Determine S-Record group"""

        if self.type == 0:
            return SRecordType.HEADER
        elif 1 <= self.type <= 3:
            return SRecordType.DATA
        elif self.type == 5:
            return SRecordType.COUNT
        elif 7 <= self.type <= 9:
            return SRecordType.TERMINATION
        else:
            return SRecordType.UNKNOWN

    def data_len(self):
        """Get data length in bytes for the S-Record"""

        return len(self.data)

    def length(self):
        """Get the S-Record length in bytes"""

        len_addr = 0 if self.address is None else self.address_len()
        len_data = 0 if self.data is None else self.data_len()
        return 3 + len_addr + len_data


    def calc_crc(self):
        """Calculate S-Record checksum"""

        # return low order byte of the complement of the sum of bytes
        return ord(struct.pack('<h', ~sum(self.data))[:1])

    def build_str(self, color=False):
        return self.__str__(color=color)

    def __str__(self, color=False):
        str_addr = ''
        if self.address is not None:
            str_addr = '{1:0{0}X}'.format(self.address_len(), self.address)

        str_data = ''
        if self.data is not None:
            str_data = binascii.hexlify(bytes(bytearray(self.data))).decode('ascii').upper()

        if not color:
            return 'S{:X}{:02X}{}{}{:02X}'.format(self.type, self.count, str_addr, str_data, self.crc)
        else:
            return '{}S{:X}{}{:02X}{}{}{}{}{}{:02X}{}'.format(fore.RED,self.type,
                                                  fore.YELLOW, self.count,
                                                  fore.GREEN, str_addr,
                                                  fore.LIGHT_BLUE, str_data,
                                                  fore.YELLOW, self.crc,
                                                  style.RESET)