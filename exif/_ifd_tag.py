"""IFD tag structure parser module."""

import binascii
import struct

from exif._constants import (EXIF_POINTER_TAG_ID, GPS_POINTER_TAG_ID, EXIF_LITTLE_ENDIAN_HEADER,
                             EXIF_BIG_ENDIAN_HEADER)


class IfdTag(object):

    """IFD tag structure parser class."""

    def __init__(self, endianess, tag_hex):
        self._format = None
        if endianess == EXIF_LITTLE_ENDIAN_HEADER:
            self._format = "<HHII"
            self.endian_prefix = '<'
        if endianess == EXIF_BIG_ENDIAN_HEADER:
            self._format = ">HHII"
            self.endian_prefix = '>'

        self.tag, self.dtype, self.count, self.value_offset = struct.unpack(
            self._format, binascii.unhexlify(tag_hex))

    def is_exif_pointer(self):
        """Determine if this IFD tag is an EXIF pointer.

        :returns: is EXIF pointer
        :rtype: bool

        """
        return self.tag == EXIF_POINTER_TAG_ID

    def is_gps_pointer(self):
        """Determine if this IFD tag is an GPS pointer.

        :returns: is GPS pointer
        :rtype: bool

        """
        return self.tag == GPS_POINTER_TAG_ID
