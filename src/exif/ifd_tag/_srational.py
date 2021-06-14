"""IFD SRATIONAL tag structure parser module."""

from fractions import Fraction

from plum.bigendian import sint32
from plum.littleendian import sint32 as sint32_le
from plum.structure import member, Structure

from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class SrationalDtype(Structure):

    """SRATIONAL Datatype"""

    numerator: int = member(fmt=sint32)
    denominator: int = member(fmt=sint32)


class SrationalDtypeLe(Structure):

    """SRATIONAL Datatype (Little Endian)"""

    numerator: int = member(fmt=sint32_le)
    denominator: int = member(fmt=sint32_le)


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

        srational_view = self.srational_dtype_cls.view(
            self._app1_ref.body_bytes, int(self.tag_view.value_offset)
        )
        srational_view.numerator.set(fraction.numerator)
        srational_view.denominator.set(fraction.denominator)

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SRATIONAL type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        srational_view = self.srational_dtype_cls.view(
            self._app1_ref.body_bytes, int(self.tag_view.value_offset)
        )
        return srational_view.numerator / srational_view.denominator

    def wipe(self):
        """Wipe value pointer target bytes to null."""
        srational_view = self.srational_dtype_cls.view(
            self._app1_ref.body_bytes, int(self.tag_view.value_offset)
        )
        srational_view.numerator.set(0)
        srational_view.denominator.set(0)
