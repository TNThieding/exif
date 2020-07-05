"""APP1 metadata interface module for EXIF tags."""

from plum import unpack_from

from exif._constants import ATTRIBUTE_ID_MAP, ATTRIBUTE_NAME_MAP, ATTRIBUTE_TYPE_MAP, ERROR_IMG_NO_ATTR, ExifMarkers
from exif._datatypes import ExifType, ExifTypeLe, Ifd, IfdLe, IfdTag, IfdTagLe, TiffByteOrder, TiffHeader

from exif.ifd_tag import (
    Ascii, BaseIfdTag, Byte, ExifVersion, Long, Rational, Short, Slong, Srational, UserComment, WindowsXp)


class App1MetaData:

    """APP1 metadata interface class for EXIF tags."""

    def _add_tag(self, tag, value):
        try:
            tag_type, ifd_number = ATTRIBUTE_TYPE_MAP[tag]
        except KeyError:
            raise AttributeError("cannot add attribute {0} to image".format(tag))

        if self.endianness == TiffByteOrder.BIG:
            ifd_cls = Ifd
            ifd_tag_cls = IfdTag
        else:
            ifd_cls = IfdLe
            ifd_tag_cls = IfdTagLe

        target_ifd_offset = self.ifd_pointers[ifd_number]
        orig_ifd = unpack_from(ifd_cls, self.body_bytes, offset=target_ifd_offset)

        offset_after_ifd = target_ifd_offset + orig_ifd.nbytes
        if not self.body_bytes[offset_after_ifd:offset_after_ifd + IfdTag.nbytes] == b"\x00" * IfdTag.nbytes:
            raise RuntimeError("destination IFD ({0}) does not have space for an additional tag".format(ifd_number))

        tags = list(orig_ifd.tags)
        tags.append(ifd_tag_cls(  # FUTURE: Find a valid value offset if a pointer type!
            tag_id=ATTRIBUTE_ID_MAP[tag], type=tag_type, value_count=1, value_offset=0))  # value set later

        # Pack in new IFD bytes. (Note: The pack_into method overrides the pre-existing bytes.)
        new_ifd = ifd_cls(tags=tags, next=orig_ifd.next)
        new_ifd.pack_into(self.body_bytes, offset=target_ifd_offset)

        # Reload to pick up on new bytes arrangement and then modify the currently-zero value.
        self._parse_ifd_segments()
        self.ifd_tags[ATTRIBUTE_ID_MAP[tag]].modify(value)

    def _delete_ifd_tag(self, attribute_id):
        # Overwrite pointer data with null bytes (if applicable, depending on datatype).
        self.ifd_tags[attribute_id].wipe()

        # Unpack the original IFD section.
        corresponding_ifd_offset = self.ifd_pointers[self.tag_parent_ifd[attribute_id]]
        if self.endianness == TiffByteOrder.BIG:
            ifd_cls = Ifd
        else:
            ifd_cls = IfdLe
        orig_ifd = unpack_from(ifd_cls, self.body_bytes, offset=corresponding_ifd_offset)

        # Construct a new IFD section datatype containing all tags but the deletion target.
        preserved_tags = [tag for tag in orig_ifd.tags if tag.tag_id != attribute_id]
        new_ifd = ifd_cls(tags=preserved_tags, next=orig_ifd.next)

        # Pack in new IFD bytes with null bytes (i.e., an empty IFD tag) appended to preserve pointers.
        # Note: The pack_into method overrides the pre-existing bytes.
        new_ifd.pack_into(self.body_bytes, offset=corresponding_ifd_offset)
        IfdTag(0, 0, 0, 0).pack_into(self.body_bytes, offset=corresponding_ifd_offset + new_ifd.nbytes)

        # Remove tag from parser tag dictionary.
        del self.ifd_tags[attribute_id]
        del self.tag_parent_ifd[attribute_id]

        # Regenerate information about existing tags.
        self._parse_ifd_segments()

    def _extract_thumbnail(self):
        if 1 in self.ifd_pointers:  # IFD segment 1 contains thumbnail (if present)
            hex_after_ifd1 = self.body_bytes[self.ifd_pointers[1]:]
            try:
                start_index = hex_after_ifd1.index(ExifMarkers.SOI)
                end_index = hex_after_ifd1.index(ExifMarkers.EOI) + len(ExifMarkers.EOI)
            except ValueError:
                pass  # no thumbnail
            else:
                self.thumbnail_bytes = hex_after_ifd1[start_index:end_index]

    def get_segment_bytes(self):
        """Get equivalent APP1 segment bytes.

        :returns: segment bytes
        :rtype: bytes

        """
        return bytes(self.header_bytes) + bytes(self.body_bytes)

    def get_tag_list(self):
        """Get a list of EXIF tag attributes present in the image object.

        :returns: image EXIF tag names
        :rtype: list of str

        """
        return [ATTRIBUTE_NAME_MAP.get(key, "<unknown EXIF tag {0}>".format(key))
                for key in self.ifd_tags]

    def _iter_ifd_tags(self, ifd_key):
        ifd_offset = self.ifd_pointers[ifd_key]

        if self.endianness == TiffByteOrder.BIG:
            ifd_t = unpack_from(Ifd, self.body_bytes, offset=ifd_offset)
        else:
            ifd_t = unpack_from(IfdLe, self.body_bytes, offset=ifd_offset)

        for tag_index in range(ifd_t.count):
            tag_offset = ifd_offset + 2 + tag_index * IfdTag.nbytes  # count is 2 bytes
            tag_t = ifd_t.tags[tag_index]
            tag_py_ins = self._tag_factory(ifd_t.tags[tag_index], tag_offset)

            if ifd_key != 1 or tag_t.tag_id not in self.ifd_tags:  # don't let thumbnail tags override base image tags
                self.ifd_tags[tag_t.tag_id] = tag_py_ins
                self.tag_parent_ifd[tag_t.tag_id] = ifd_key

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
            current_ifd_offset = self._iter_ifd_tags(current_ifd)
            current_ifd += 1

        if "exif" in self.ifd_pointers:
            self._iter_ifd_tags("exif")

        if "gps" in self.ifd_pointers:
            self._iter_ifd_tags("gps")

    def _tag_factory(self, tag_t, offset):  # pylint: disable=too-many-branches
        if self.endianness == TiffByteOrder.BIG:
            exif_type_cls = ExifType
        else:
            exif_type_cls = ExifTypeLe

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

    def __init__(self, segment_bytes):
        self.header_bytes = bytearray(segment_bytes[:0xA])
        self.body_bytes = bytearray(segment_bytes[0xA:])

        self.endianness = None
        self.ifd_pointers = {}
        self.ifd_tags = {}
        self.tag_parent_ifd = {}
        self.thumbnail_bytes = None

        self._parse_ifd_segments()
        self._extract_thumbnail()

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
                self.ifd_tags[attribute_id]
            except KeyError:
                raise AttributeError(ERROR_IMG_NO_ATTR.format(item))

            self._delete_ifd_tag(attribute_id)

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
                # Tag is not in image already.
                self._add_tag(key, value)
            else:
                ifd_tag.modify(value)
