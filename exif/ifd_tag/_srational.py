"""IFD SRATIONAL tag structure parser module."""

from fractions import Fraction

from plum.int.big import SInt32
from plum.int.little import SInt32 as SInt32Le
from plum.structure import Member, Structure

from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class SrationalDtype(Structure):

    """SRATIONAL Datatype"""

    numerator: int = Member(cls=SInt32)
    denominator: int = Member(cls=SInt32)


class SrationalDtypeLe(Structure):

    """SRATIONAL Datatype (Little Endian)"""

    numerator: int = Member(cls=SInt32Le)
    denominator: int = Member(cls=SInt32Le)


class Srational(BaseIfdTag):

    """IFD SRATIONAL tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self.srational_dtype_cls = SrationalDtype
        else:
            self.srational_dtype_cls = SrationalDtypeLe

    def modify(self, value):
        """Modify tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SRATIONAL type with a count greater than 1.

        :param value: new tag value
        :type value: corresponding Python type

        """
        fraction = Fraction(value).limit_denominator()

        srational_view = self.srational_dtype_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.get())
        srational_view.numerator.set(fraction.numerator)
        srational_view.denominator.set(fraction.denominator)

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SRATIONAL type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        srational_view = self.srational_dtype_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.get())
        return srational_view.numerator / srational_view.denominator

    def wipe(self):
        """Wipe value pointer target bytes to null."""
        srational_view = self.srational_dtype_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.get())
        srational_view.numerator.set(0)
        srational_view.denominator.set(0)
