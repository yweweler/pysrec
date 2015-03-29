from enum import Enum
from zwuenf.pysrec import SRECError


class SRecordType(Enum):
    HEADER = 0
    DATA = 1
    COUNT = 2
    TERMINATION = 3
    UNKNOWN = 4


class SRecord:
    """Data srtructure fot holding SRecords"""

    def __init__(self, str):
        """SRecord constructor"""
        self.__min_record_len = 10
        self.__default_addr_len = 6

        self.type = 0x00
        self.__count = 0x00
        self.__address = 0x00
        self.__data = 0x00
        self.__crc = 0x00
        self.__length = len(str)

        self.__parse__(str)

    def __str__(self):
        addr = ''
        if self.__address is not None:
            addr = '{1:0{0}X}'.format(self.addr_len(), self.__address)

        data = ''
        if self.__data is not None:
            data = '{1:0{0}X}'.format(self.data_len(), self.__data)

        return ('S{:X}{:02X}{}{}{:02X}').format(self.type,
                                      self.__count,
                                      addr,
                                      data,
                                      self.__crc)

    def __parse__(self, str):
        """Parse SRecord from string"""
        str = str.strip('\r\n')
        if len(str) <= self.__min_record_len:
            raise SRECError

        try:
            self.type = int(str[1:2], 16)

            self.__count = int(str[2:4], 16)

            addr_str = str[4:4+self.addr_len()]
            self.__address = None
            if len(addr_str) is not 0:
                self.__address = int(addr_str, 16)

            data_str = str[4+self.addr_len():-2]
            self.__data = None
            if len(data_str) is not 0:
                self.__data = int(data_str, 16)

            self.__crc = int(str[-2:], 16)
        except:
            raise SRECError

    def length(self):
        """Return the Srecord length in bytes"""
        return self.__length

    def record_group(self):
        """Determine SRecord group"""
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

    def calc_crc(self):
        """Calculate SRecord checksum"""
        # TODO
        return 0x00

    def addr_len(self):
        """Get address length for the SRecord"""
        # TODO
        if self.record_group() is SRecordType.DATA:
            return (self.type + 1) * 2
        else:
            return self.__default_addr_len

    def data_len(self):
        """Get data length for the SRecord"""
        return self.length() - (6 + self.addr_len())