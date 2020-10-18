"""IFD RATIONAL tag structure parser module."""

from fractions import Fraction

from plum.int.big import UInt32
from plum.int.little import UInt32 as UInt32Le
from plum.structure import Member, Structure

from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class RationalDtype(Structure):

    """RATIONAL Datatype"""

    numerator: int = Member(cls=UInt32)
    denominator: int = Member(cls=UInt32)


class RationalDtypeLe(Structure):

    """RATIONAL Datatype (Little Endian)"""

    numerator: int = Member(cls=UInt32Le)
    denominator: int = Member(cls=UInt32Le)


class Rational(BaseIfdTag):

    """IFD RATIONAL tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self.rational_dtype_cls = RationalDtype
        else:
            self.rational_dtype_cls = RationalDtypeLe

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == self.tag_view.value_count.get()
        else:
            assert self.tag_view.value_count.get() == 1
            value = (value,)

        for rational_index in range(self.tag_view.value_count.get()):
            current_offset = self.tag_view.value_offset.get() + rational_index * self.rational_dtype_cls.nbytes
            rational_view = self.rational_dtype_cls.view(self._app1_ref.body_bytes, current_offset)

            if isinstance(value[rational_index], int) and value[rational_index] == 0:
                # EXIF 2.3 Specification: "When a value is unknown, the notation is 0/0" (e.g., lens specification).
                rational_view.numerator.set(0)
                rational_view.denominator.set(0)
            else:
                fraction = Fraction(value[rational_index]).limit_denominator()
                rational_view.numerator.set(fraction.numerator)
                rational_view.denominator.set(fraction.denominator)

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []

        for rational_index in range(self.tag_view.value_count.get()):
            current_offset = self.tag_view.value_offset.get() + rational_index * self.rational_dtype_cls.nbytes
            rational_view = self.rational_dtype_cls.view(self._app1_ref.body_bytes, current_offset)

            if rational_view.numerator == 0 and rational_view.denominator == 0:
                # EXIF 2.3 Specification: "When a value is unknown, the notation is 0/0" (e.g., lens specification).
                retvals.append(0)
            else:
                retvals.append(rational_view.numerator / rational_view.denominator)

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval

    def wipe(self):
        """Wipe value pointer target bytes to null."""
        for rational_index in range(self.tag_view.value_count.get()):
            current_offset = self.tag_view.value_offset.get() + rational_index * self.rational_dtype_cls.nbytes
            rational_view = self.rational_dtype_cls.view(self._app1_ref.body_bytes, current_offset)

            rational_view.numerator.set(0)
            rational_view.denominator.set(0)
