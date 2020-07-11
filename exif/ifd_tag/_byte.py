"""IFD BYTE tag structure parser module."""

from plum.int.big import UInt8
from plum.int.little import UInt8 as UInt8_L

from exif._constants import ATTRIBUTE_ID_MAP, GpsAltitudeRef
from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class Byte(BaseIfdTag):

    """IFD BYTE tag structure parser class."""

    ENUMS_MAP = {
        ATTRIBUTE_ID_MAP["gps_altitude_ref"]: GpsAltitudeRef,
    }

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._uint8_cls = UInt8
        else:
            self._uint8_cls = UInt8_L

    def modify(self, value):
        """Modify tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of BYTE type with a count greater than 1.

        :param value: new tag value
        :type value: corresponding Python type

        """
        self._uint8_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.__offset__).set(int(value))

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of BYTE type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retval = self._uint8_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.__offset__).get()

        if int(self.tag_view.tag_id) in self.ENUMS_MAP:
            retval = self.ENUMS_MAP[int(self.tag_view.tag_id)](retval)

        return retval
