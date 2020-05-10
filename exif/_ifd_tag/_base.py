"""Base IFD tag structure parser module."""

from exif._constants import EXIF_LITTLE_ENDIAN_HEADER, EXIF_POINTER_TAG_ID, GPS_POINTER_TAG_ID


class Base:

    """Base IFD tag structure parser class."""

    def __init__(self, tag, count, value_offset, section_start_address, parent_segment_hex,
                 value_offset_addr):
        self.tag = int(tag, 16)
        self.count = int(count, 16)
        self.value_offset = int(value_offset, 16)
        self.section_start_address = section_start_address
        self.parent_segment_hex = parent_segment_hex
        self.value_offset_addr = value_offset_addr

        if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
            self.struct_index = -1
        else:
            self.struct_index = 0

    def __eq__(self, other):
        return self.tag == other.tag

    def __repr__(self):
        return "_ifd_tag.Base(tag={}, count={}, value_offset={}, section_start_address={})".format(
            self.tag, self.count, self.value_offset, self.section_start_address)

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

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError("cannot modify a base/unknown IFD tag instance")

    def read(self):  # pragma: no cover
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        raise NotImplementedError("cannot read a base/unknown IFD tag instance")
