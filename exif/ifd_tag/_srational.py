"""IFD SRATIONAL tag structure parser module."""

import binascii
import struct
from fractions import Fraction

from plum.int.big import SInt32
from plum.int.little import SInt32 as SInt32_L
from plum.structure import Member, Structure

from exif._constants import EXIF_LITTLE_ENDIAN_HEADER
from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class SrationalDtype(Structure):
    numerator: int = Member(cls=SInt32)
    denominator: int = Member(cls=SInt32)


class SrationalDtype_L(Structure):
    numerator: int = Member(cls=SInt32_L)
    denominator: int = Member(cls=SInt32_L)


class Srational(BaseIfdTag):

    """IFD SRATIONAL tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self.srational_dtype_cls = SrationalDtype
        else:
            self.srational_dtype_cls = SrationalDtype_L

    def modify(self, value):
        """Modify tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SRATIONAL type with a count greater than 1.

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

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SRATIONAL type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        srational_view = self.srational_dtype_cls.view(self._app1_ref.body_bytes, self._tag_view.value_offset.get())
        return srational_view.numerator / srational_view.denominator
