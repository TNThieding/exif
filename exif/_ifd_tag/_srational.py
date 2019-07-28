"""IFD SRATIONAL tag structure parser module."""

import binascii
import struct
from fractions import Fraction

from exif._constants import EXIF_LITTLE_ENDIAN_HEADER
from exif._ifd_tag._base import Base as BaseIfdTag


class Srational(BaseIfdTag):

    """IFD SRATIONAL tag structure parser class."""

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == self.count
        else:
            assert self.count == 1
            value = (value,)

        cursor = 0xA + self.value_offset
        for member_index in range(self.count):
            fraction = Fraction(value[member_index]).limit_denominator()

            if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                new_member_bits = struct.pack(
                    ">ll", fraction.denominator, fraction.numerator)
            else:
                new_member_bits = struct.pack(
                    ">ll", fraction.numerator, fraction.denominator)

            new_member_hex = binascii.hexlify(new_member_bits)
            self.parent_segment_hex.modify_hex(cursor, new_member_hex)
            cursor += 8

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []
        cursor = 0xA + self.value_offset

        for member_index in range(self.count):  # pylint: disable=unused-variable
            data_format = ">ll"
            numerator, denominator = struct.unpack(data_format, binascii.unhexlify(
                self.parent_segment_hex.read(cursor, 8)))
            cursor += 8
            if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                retvals.append(float(denominator) / float(numerator))
            else:
                retvals.append(float(numerator) / float(denominator))

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval
