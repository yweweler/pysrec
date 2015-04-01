import os

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
    """Data structure for holding SRecords"""

    def __init__(self, file):
        """SRecordFile constructor"""

        self.__records = list()
        self.__count = None

        self.__parse__(file)
        self.__length = os.path.getsize(file)

    def __parse__(self, file):
        """Parse a S-Record file"""

        self.__records = list()
        with open(file) as f:
            for line in f:
                # TODO: if first byte os 0xFF or something like that, python will fail here!
                if not line[0] == 'S':
                    raise NotSRecFileError

                self.__records.append(SRecord(line))

    def length(self):
        """Return the S-Record file length in bytes"""

        return self.__length

    def lines(self):
        """Return the S-Record file length in lines"""

        return len(self.__records)

    # TODO: test
    def mot_type(self):
        """Determine files MOT type"""
        for record in self.__records:
            if record.record_group() == SRecordType.UNKNOWN:
                return MOTType.UNKNOWN

        if self.__count is None:
            self.record_counts()

        s19 = self.__count[1] + self.__count[9]
        s28 = self.__count[2] + self.__count[8]
        s37 = self.__count[3] + self.__count[7]

        sum = s19 + s28 + s37
        if sum == s19 or sum == s28 or sum == s37:
            if sum == s19:
                return MOTType.S19
            elif sum == s28:
                return MOTType.S28
            else:
                return MOTType.S37

        return MOTType.UNKNOWN

    # TODO: test
    def record_counts(self):
        """Count Record types"""
        self.__count = dict()
        for record in self.__records:
            if record.type not in self.__count:
                self.__count[record.type] = 0

            self.__count[record.type] += 1

        return self.__count

    def has_header(self):
        # TODO: test
        if self.__count is None:
            self.record_counts()

        if self.__count[0] > 0:
            return True

        return False

    def min_address(self):
        # TODO: test
        addr = self.__records[0]
        for record in self.__records:
            addr = min(addr, record.address)

    def max_address(self):
        # TODO: test
        addr = self.__records[0]
        for record in self.__records:
            addr = max(addr, record.address)