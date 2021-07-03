import os
import binascii

__all__ = ('MOTType', 'SRecordFile')

from enum import Enum
from zwuenf.pysrec.SRecord import SRecordType, SRecord
from zwuenf.pysrec import *


class MOTType(Enum):
    S19 = 0
    S28 = 1
    S37 = 2
    UNKNOWN = 3


class SRecordFile:
    """Data structure for holding a S-Record file."""

    def __init__(self, file):
        """SRecordFile constructor."""

        self.__path = file
        self.__count = None
        self.records = list()

        self.__parse__(file)

    def __parse__(self, file):
        """Parse a S-Record file."""

        self.records = list()
        with open(file) as f:
            for line in f:
                # TODO: if first byte is 0xFF or something like that, python will fail here!
                if not line[0] == 'S':
                    raise NotSRecFileError

                self.records.append(SRecord(line))

    def size(self):
        """Return the S-Record file size in bytes."""

        return os.path.getsize(self.__path)

    def lines(self):
        """Return the S-Record file length in lines."""

        return len(self.records)

    def mot_type(self):
        """Determine files MOT type."""

        for record in self.records:
            if record.record_group() == SRecordType.UNKNOWN:
                return MOTType.UNKNOWN

        if self.__count is None:
            self.record_counts()

        s19 = s28 = s37 = 0

        if 1 in self.__count and 9 in self.__count:
            s19 = self.__count[1] + self.__count[9]

        if 2 in self.__count and 8 in self.__count:
            s28 = self.__count[2] + self.__count[8]

        if 3 in self.__count and 7 in self.__count:
            s37 = self.__count[3] + self.__count[7]

        s = s19 + s28 + s37
        if s == s19 or s == s28 or s == s37:
            if s == s19:
                return MOTType.S19
            elif s == s28:
                return MOTType.S28
            else:
                return MOTType.S37

        return MOTType.UNKNOWN

    def record_counts(self):
        """Count record types."""

        self.__count = dict()
        for record in self.records:
            if record.type not in self.__count:
                self.__count[record.type] = 0

            self.__count[record.type] += 1

        return self.__count

    def has_header(self):
        """Check if S-Record file has a header record."""

        if self.__count is None:
            self.record_counts()

        if 0 in self.__count and self.__count[0] > 0:
            return True

        return False

    def min_address(self):
        """Get the lowest address in the file."""

        addr = self.records[0].address
        for record in self.records:
            addr = min(addr, record.address)

        return addr

    def max_address(self):
        """Get the highest address in the file."""

        addr = self.records[0].address
        for record in self.records:
            addr = max(addr, record.address)

        return addr

    def header_content(self):
        """Get the content of the header record as a string."""

        if not self.has_header():
            pass

        return binascii.unhexlify(binascii.hexlify(bytes(bytearray(self.records[0].data)))).decode('ascii')

    def write_binary(self, path):
        """Generate a binary file from the S-Record file."""

        with open(path, "wb") as _fp:
            for r in self.records:
                if r.type not in [1, 2, 3]:
                    # Not a data type; we don't need it to write binary rom
                    # print("skipping type %s (%s)" % (r.type, str(r)))
                    continue
                if r.type in [2, 3]:
                    raise Exception("Types 2 and 3 haven't been tested yet")
                _fp.seek(r.address)
                for d in r.data:
                    _fp.write(d)
