"""IFD BYTE tag structure parser module."""

from plum.int.big import UInt8
from plum.int.little import UInt8 as UInt8_L

from exif._datatypes import IfdTag, IfdTag_L, TiffByteOrder
from exif._ifd_tag._base import Base as BaseIfdTag


class Byte(BaseIfdTag):

    """IFD BYTE tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._uint8_cls = UInt8
        else:
            self._uint8_cls = UInt8_L

    def modify(self, value):  # pragma: no cover
        raise NotImplementedError("this package does not yet support setting BYTE tags")

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of BYTE type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        tag_view = self._ifd_tag_cls.view(self._app1_ref.body_bytes, self._tag_offset)
        return self._uint8_cls.view(self._app1_ref.body_bytes, tag_view.value_offset.__offset__).get()
