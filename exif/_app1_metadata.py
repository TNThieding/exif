"""APP1 metadata interface module for EXIF tags."""

from plum import unpack_from

from exif._constants import (
    ATTRIBUTE_ID_MAP, ATTRIBUTE_NAME_MAP, BYTES_PER_IFD_TAG_COUNT, BYTES_PER_IFD_TAG_ID,
    BYTES_PER_IFD_TAG_TYPE, BYTES_PER_IFD_TAG_VALUE_OFFSET, BYTES_PER_IFD_TAG_TOTAL,
    ERROR_IMG_NO_ATTR, ExifMarkers)
from exif._datatypes import ExifType, ExifType_L, Ifd, Ifd_L, IfdTag, IfdTag_L, TiffByteOrder, TiffHeader

from exif.ifd_tag import (
    Ascii, BaseIfdTag, Byte, ExifVersion, Long, Rational, Short, Slong, Srational, UserComment, WindowsXp)


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
        if isinstance(delete_target, Ascii) and delete_target.count > 4:
            self._segment_hex.wipe(cursor, delete_target.count)
        if isinstance(delete_target, (Srational, Rational)):  # 8 Bytes
            self._segment_hex.wipe(cursor, delete_target.count * 8)

        # Remove tag from parser tag dictionary.
        del self.ifd_tags[ifd_tag.tag]

    def get_segment_bytes(self):
        """Get equivalent APP1 segment bytes.

        :returns: segment bytes
        :rtype: bytes

        """
        return bytes(self.header_bytes) + bytes(self.body_bytes)

    def get_tag_list(self):
        """Get a list of EXIF tag attributes present in the image objec.

        :returns: image EXIF tag names
        :rtype: list of str

        """
        return [ATTRIBUTE_NAME_MAP.get(key, "<unknown EXIF tag {0}>".format(key))
                for key in self.ifd_tags]

    def _tag_factory(self, tag_t, offset):
        if self.endianness == TiffByteOrder.BIG:
            exif_type_cls = ExifType
        else:
            exif_type_cls = ExifType_L

        if ATTRIBUTE_ID_MAP["xp_title"] <= tag_t.tag_id <= ATTRIBUTE_ID_MAP["xp_subject"]:  # legacy Windows XP tags
            cls = WindowsXp
        elif ATTRIBUTE_ID_MAP["exif_version"] == tag_t.tag_id:  # custom ASCII encoding without termination character
            cls = ExifVersion
        elif ATTRIBUTE_ID_MAP["user_comment"] == tag_t.tag_id:
            cls = UserComment
        elif tag_t.type == exif_type_cls.BYTE:
            cls = Byte
        elif tag_t.type == exif_type_cls.ASCII:
            cls = Ascii
        elif tag_t.type == exif_type_cls.SHORT:
            cls = Short
        elif tag_t.type == exif_type_cls.LONG:
            cls = Long
        elif tag_t.type == exif_type_cls.RATIONAL:
            cls = Rational
        elif tag_t.type == exif_type_cls.SLONG:
            cls = Slong
        elif tag_t.type == exif_type_cls.SRATIONAL:
            cls = Srational
        else:
            cls = BaseIfdTag

        return cls(offset, self)

    def _iter_ifd_tags(self, ifd_offset):
        if self.endianness == TiffByteOrder.BIG:
            ifd_t = unpack_from(Ifd, self.body_bytes, offset=ifd_offset)
        else:
            ifd_t = unpack_from(Ifd_L, self.body_bytes, offset=ifd_offset)

        for tag_index in range(ifd_t.count):
            tag_offset = ifd_offset + 2 + tag_index * IfdTag.nbytes  # count is 2 bytes
            tag_t = ifd_t.tags[tag_index]
            tag_py_ins = self._tag_factory(ifd_t.tags[tag_index], tag_offset)

            self.ifd_tags[tag_t.tag_id] = tag_py_ins

            if tag_t.tag_id == ATTRIBUTE_ID_MAP["_exif_ifd_pointer"]:
                self.ifd_pointers["exif"] = tag_t.value_offset

            if tag_t.tag_id == ATTRIBUTE_ID_MAP["_gps_ifd_pointer"]:
                self.ifd_pointers["gps"] = tag_t.value_offset

        return ifd_t.next

    def _parse_ifd_segments(self):
        tiff_header = unpack_from(TiffHeader, self.body_bytes)
        self.endianness = tiff_header.byte_order

        current_ifd = 0
        current_ifd_offset = tiff_header.ifd_offset

        while current_ifd_offset:
            self.ifd_pointers[current_ifd] = current_ifd_offset
            current_ifd_offset = self._iter_ifd_tags(current_ifd_offset)
            current_ifd += 1

        if "exif" in self.ifd_pointers:
            self._iter_ifd_tags(self.ifd_pointers["exif"])

        if "gps" in self.ifd_pointers:
            self._iter_ifd_tags(self.ifd_pointers["gps"])

        #
        #     if current_ifd == 1:  # TODO: IFD segment 1 contains thumbnail (if present)
        #         succeeding_hex_string = self._segment_hex.get_hex_string()[cursor * HEX_PER_BYTE:]
        #         try:
        #             start_index = succeeding_hex_string.index(ExifMarkers.SOI)
        #             end_index = succeeding_hex_string.index(ExifMarkers.EOI) + len(ExifMarkers.EOI)
        #         except ValueError:
        #             pass  # no thumbnail
        #         else:
        #             self.thumbnail_hex_string = succeeding_hex_string[start_index:end_index]

    def __init__(self, segment_bytes):
        self.header_bytes = bytearray(segment_bytes[:0xA])
        self.body_bytes = bytearray(segment_bytes[0xA:])

        self.endianness = None
        self.ifd_pointers = {}
        self.ifd_tags = {}
        self.thumbnail_bytes = None

        self._parse_ifd_segments()

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
