"""IFD RATIONAL tag structure parser module."""

import binascii
import struct
from fractions import Fraction

from plum.int.big import UInt32
from plum.int.little import UInt32 as UInt32_L
from plum.structure import Member, Structure

from exif._constants import EXIF_LITTLE_ENDIAN_HEADER
from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class RationalDtype(Structure):
    numerator: int = Member(cls=UInt32)
    denominator: int = Member(cls=UInt32)


class RationalDtype_L(Structure):
    numerator: int = Member(cls=UInt32_L)
    denominator: int = Member(cls=UInt32_L)


class Rational(BaseIfdTag):

    """IFD RATIONAL tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self.rational_dtype_cls = RationalDtype
        else:
            self.rational_dtype_cls = RationalDtype_L

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == self._tag_view.value_count.get()
        else:
            assert self._tag_view.value_count.get() == 1
            value = (value,)

        for rational_index in range(self._tag_view.value_count.get()):
            current_offset = self._tag_view.value_offset.get() + rational_index * self.rational_dtype_cls.nbytes
            rational_view = self.rational_dtype_cls.view(self._app1_ref.body_bytes, current_offset)

            fraction = Fraction(value[rational_index]).limit_denominator()
            rational_view.numerator.set(fraction.numerator)
            rational_view.denominator.set(fraction.denominator)

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []

        for rational_index in range(self._tag_view.value_count.get()):
            current_offset = self._tag_view.value_offset.get() + rational_index * self.rational_dtype_cls.nbytes
            rational_view = self.rational_dtype_cls.view(self._app1_ref.body_bytes, current_offset)
            retvals.append(rational_view.numerator / rational_view.denominator)

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval
