"""APP1 metadata interface module for EXIF tags."""

from exif._constants import (
    ATTRIBUTE_ID_MAP, ATTRIBUTE_NAME_MAP, BYTES_PER_IFD_TAG_COUNT, BYTES_PER_IFD_TAG_ID,
    BYTES_PER_IFD_TAG_TYPE, BYTES_PER_IFD_TAG_VALUE_OFFSET, BYTES_PER_IFD_TAG_TOTAL,
    ERROR_IMG_NO_ATTR, ExifTypes, USER_COMMENT_CHARACTER_CODE_LEN_BYTES)
from exif._hex_interface import HexInterface

from exif._ifd_tag._ascii import Ascii
from exif._ifd_tag._base import Base as BaseIfdTag
from exif._ifd_tag._byte import Byte
from exif._ifd_tag._long import Long
from exif._ifd_tag._rational import Rational
from exif._ifd_tag._short import Short
from exif._ifd_tag._slong import Slong
from exif._ifd_tag._srational import Srational


class App1MetaData:

    """APP1 metadata interface class for EXIF tags."""

    def _delete_ifd_tag(self, ifd_tag):
        # Get the tag count in the deletion target's IFD section.
        delete_target = self.ifd_tags[ifd_tag.tag]
        section_start_address = delete_target.section_start_address
        section_tag_count = int(self._segment_hex.read(section_start_address, 2), 16)

        # Decrease the tag count by 1 in the file hexadecimal.
        self._segment_hex.modify_number(section_start_address, 2, section_tag_count - 1)

        # Parse over the deletion target's IFD section and remove the tag.
        cursor = section_start_address + 2
        for tag_index in range(section_tag_count):  # pylint: disable=unused-variable
            tag_id = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID)
            cursor += BYTES_PER_IFD_TAG_ID
            tag_type = int(self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID), 16)
            cursor += BYTES_PER_IFD_TAG_TYPE
            tag_count = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_COUNT)
            cursor += BYTES_PER_IFD_TAG_COUNT
            tag_value_offset = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_VALUE_OFFSET)
            tag_value_offset_addr = cursor
            cursor += BYTES_PER_IFD_TAG_VALUE_OFFSET

            tag = self._tag_factory(tag_id, tag_type, tag_count, tag_value_offset,
                                    section_start_address, tag_value_offset_addr)

            if delete_target == tag:
                cursor -= BYTES_PER_IFD_TAG_TOTAL
                self._segment_hex.delete(cursor, BYTES_PER_IFD_TAG_TOTAL)

        # Pad ending of IFD section to preserve pointers.
        self._segment_hex.insert_null(cursor, BYTES_PER_IFD_TAG_TOTAL)

        # Overwrite pointer data with null bytes (if applicable, depending on datatype).
        cursor = 0xA + ifd_tag.value_offset
        if isinstance(delete_target, Ascii):
            self._segment_hex.wipe(cursor, delete_target.count)
        if isinstance(delete_target, (Srational, Rational)):  # 8 Bytes
            self._segment_hex.wipe(cursor, delete_target.count * 8)

        # Remove tag from parser tag dictionary.
        del self.ifd_tags[ifd_tag.tag]

    def get_segment_hex(self):
        """Get equivalent APP1 hexadecimal string.

        :returns: segment hexadecimal string
        :rtype: str

        """
        return self._segment_hex.get_hex_string()

    def get_tag_list(self):
        """Get a list of EXIF tag attributes present in the image objec.

        :returns: image EXIF tag names
        :rtype: list of str

        """
        return [ATTRIBUTE_NAME_MAP.get(key, "<unknown EXIF tag {0}>".format(key))
                for key in self.ifd_tags]

    def _tag_factory(self, tag_id, tag_type, tag_count, tag_value_offset, section_start_address,
                     tag_value_offset_addr):
        if tag_type == ExifTypes.BYTE:
            tag = Byte(tag_id, tag_count, tag_value_offset,
                       section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.ASCII:
            tag = Ascii(tag_id, tag_count, tag_value_offset,
                        section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.SHORT:
            tag = Short(tag_id, tag_count, tag_value_offset,
                        section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.LONG:
            tag = Long(tag_id, tag_count, tag_value_offset,
                       section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.RATIONAL:
            tag = Rational(tag_id, tag_count, tag_value_offset,
                           section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.SLONG:
            tag = Slong(tag_id, tag_count, tag_value_offset,
                        section_start_address, self._segment_hex, tag_value_offset_addr)
        elif tag_type == ExifTypes.SRATIONAL:
            tag = Srational(tag_id, tag_count, tag_value_offset,
                            section_start_address, self._segment_hex, tag_value_offset_addr)
        else:
            tag = BaseIfdTag(tag_id, tag_count, tag_value_offset,
                             section_start_address, self._segment_hex, tag_value_offset_addr)

        return tag

    def _unpack_ifd_tags(self):
        cursor = 0xA
        exif_offset = None
        gps_offset = None

        # Read the endianness specified by the image.
        self._segment_hex.set_endianness(self._segment_hex.read(cursor, 2))
        cursor += 2

        # Skip over fixed 0x002A bytes.
        cursor += 2

        # Determine the location of the first IFD section relative to the start of the APP1 section.
        # 0xA is IFD section offset from start of APP1.
        cursor = 0xA + int(self._segment_hex.read(cursor, 4), 16)

        # Read each IFD section.
        current_ifd = 0
        while cursor != 0xA:
            section_start_address = cursor
            num_ifd_tags = int(self._segment_hex.read(cursor, 2), 16)
            cursor += 2

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag_id = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID)
                cursor += BYTES_PER_IFD_TAG_ID
                tag_type = int(self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID), 16)
                cursor += BYTES_PER_IFD_TAG_TYPE
                tag_count = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_COUNT)
                cursor += BYTES_PER_IFD_TAG_COUNT
                tag_value_offset = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_VALUE_OFFSET)
                tag_value_offset_addr = cursor
                cursor += BYTES_PER_IFD_TAG_VALUE_OFFSET

                tag = self._tag_factory(tag_id, tag_type, tag_count, tag_value_offset,
                                        section_start_address, tag_value_offset_addr)

                self.ifd_tags[tag.tag] = tag

                if tag.is_exif_pointer():
                    exif_offset = tag.value_offset
                if tag.is_gps_pointer():
                    gps_offset = tag.value_offset

            next_offset_str = self._segment_hex.read(cursor, 4)

            try:
                next_offset_int = int(next_offset_str, 16)
            except ValueError:
                # Handle case of invalid literal for int() with base 16: ''
                next_offset_int = 0

            cursor = 0xA + next_offset_int
            current_ifd += 1

        # If an EXIF section pointer exists, read EXIF IFD tags.
        if exif_offset:
            cursor = 0xA + exif_offset
            section_start_address = cursor
            num_ifd_tags = int(self._segment_hex.read(cursor, 2), 16)
            cursor += 2

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag_id = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID)
                cursor += BYTES_PER_IFD_TAG_ID
                tag_type = int(self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID), 16)
                cursor += BYTES_PER_IFD_TAG_TYPE
                tag_count = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_COUNT)
                cursor += BYTES_PER_IFD_TAG_COUNT
                tag_value_offset = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_VALUE_OFFSET)
                tag_value_offset_addr = cursor
                cursor += BYTES_PER_IFD_TAG_VALUE_OFFSET

                tag = self._tag_factory(tag_id, tag_type, tag_count, tag_value_offset,
                                        section_start_address, tag_value_offset_addr)

                # Handle user comment data structure (see pg. 51 of EXIF specification).
                if tag.tag == ATTRIBUTE_ID_MAP["user_comment"]:
                    tag = Ascii(tag_id, tag_count, tag_value_offset,
                                section_start_address, self._segment_hex, tag_value_offset_addr)
                    tag.dtype = ExifTypes.ASCII  # reads unicode as well

                    tag.count += 1  # custom data structure does not use null terminator
                    tag.count -= USER_COMMENT_CHARACTER_CODE_LEN_BYTES
                    tag.value_offset += USER_COMMENT_CHARACTER_CODE_LEN_BYTES

                self.ifd_tags[tag.tag] = tag

        # If an GPS section pointer exists, read GPS IFD tags.
        if gps_offset:
            cursor = 0xA + gps_offset
            section_start_address = cursor
            num_ifd_tags = int(self._segment_hex.read(cursor, 2), 16)
            cursor += 2

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag_id = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID)
                cursor += BYTES_PER_IFD_TAG_ID
                tag_type = int(self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_ID), 16)
                cursor += BYTES_PER_IFD_TAG_TYPE
                tag_count = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_COUNT)
                cursor += BYTES_PER_IFD_TAG_COUNT
                tag_value_offset = self._segment_hex.read(cursor, BYTES_PER_IFD_TAG_VALUE_OFFSET)
                tag_value_offset_addr = cursor
                cursor += BYTES_PER_IFD_TAG_VALUE_OFFSET

                tag = self._tag_factory(tag_id, tag_type, tag_count, tag_value_offset,
                                        section_start_address, tag_value_offset_addr)

                self.ifd_tags[tag.tag] = tag

    def __init__(self, segment_hex):
        self._segment_hex = HexInterface(segment_hex)
        self.ifd_tags = {}

        self._unpack_ifd_tags()

    def __delattr__(self, item):
        try:
            # Determine if attribute is an IFD tag accessor.
            attribute_id = ATTRIBUTE_ID_MAP[item]
        except KeyError:  # pragma: no cover
            # Coverage and behavior tested by Image class.
            # Attribute is a class member. Delete natively.
            super(App1MetaData, self).__delattr__(item)
        else:
            # Attribute is not a class member. Delete EXIF tag value.
            try:
                ifd_tag = self.ifd_tags[attribute_id]
            except KeyError:
                raise AttributeError(ERROR_IMG_NO_ATTR.format(item))

            self._delete_ifd_tag(ifd_tag)

    def __getattr__(self, item):
        """If attribute is not a class member, get the value of the EXIF tag of the same name."""
        try:
            attribute_id = ATTRIBUTE_ID_MAP[item]
        except KeyError:
            raise AttributeError("unknown image attribute {0}".format(item))

        try:
            ifd_tag = self.ifd_tags[attribute_id]
        except KeyError:
            raise AttributeError(ERROR_IMG_NO_ATTR.format(item))

        return ifd_tag.read()

    def __setattr__(self, key, value):
        try:
            # Determine if attribute is an IFD tag accessor.
            attribute_id = ATTRIBUTE_ID_MAP[key]
        except KeyError:
            # Attribute is a class member. Set natively.
            super(App1MetaData, self).__setattr__(key, value)
        else:
            try:
                ifd_tag = self.ifd_tags[attribute_id]
            except KeyError:
                raise AttributeError(ERROR_IMG_NO_ATTR.format(key))

            ifd_tag.modify(value)
