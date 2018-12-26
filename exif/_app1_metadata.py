"""APP1 metadata interface module for EXIF tags."""

import binascii
import struct
import sys
from fractions import Fraction

from exif._constants import (
    ATTRIBUTE_ID_MAP, ExifTypes, HEX_PER_BYTE, ERROR_IMG_NO_ATTR, BYTES_PER_IFD_TAG)
from exif._ifd_tag import IfdTag


class App1MetaData(object):

    """APP1 metadata interface class for EXIF tags."""

    def _delete_ifd_tag(self, ifd_tag):
        # Get the tag count in the deletion target's IFD section.
        delete_target = self.ifd_tags[ifd_tag.tag]
        section_start_address = delete_target.section_start_address
        section_tag_count = int(
            self.segment_hex[section_start_address:section_start_address + 2 * HEX_PER_BYTE], 16)

        # Decrease the tag count by 1 in the file hexadecimal.
        self.segment_hex = (self.segment_hex[:section_start_address] +
                            hex(section_tag_count - 1).lstrip('0x').zfill(4) +
                            self.segment_hex[section_start_address + 2 * HEX_PER_BYTE:])

        # Parse over the deletion target's IFD section and remove the tag.
        cursor = section_start_address + 2 * HEX_PER_BYTE
        for tag_index in range(section_tag_count):  # pylint: disable=unused-variable
            tag = IfdTag(
                self._endianness,
                self.segment_hex[cursor:cursor + BYTES_PER_IFD_TAG * HEX_PER_BYTE],
                section_start_address)
            if delete_target == tag:
                self.segment_hex = (
                    self.segment_hex[:cursor] +
                    self.segment_hex[cursor + BYTES_PER_IFD_TAG * HEX_PER_BYTE:])
            else:
                cursor += BYTES_PER_IFD_TAG * HEX_PER_BYTE

        #  Pad ending of IFD section to preserve pointers.
        self.segment_hex = (
            self.segment_hex[:cursor] + '00' * BYTES_PER_IFD_TAG + self.segment_hex[cursor:])

        # Overwrite pointer data with null bytes (if applicable, depending on datatype).
        if delete_target.dtype in [ExifTypes.ASCII, ExifTypes.RATIONAL, ExifTypes.SRATIONAL]:
            cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
            if delete_target.dtype == ExifTypes.ASCII:
                null_data = '00' * delete_target.count
            else:  # SRATIONAL or RATIONAL
                null_data = '00' * 8 * delete_target.count
            self.segment_hex = (self.segment_hex[:cursor] + null_data +
                                self.segment_hex[cursor + len(null_data):])

        # Remove tag from parser tag dictionary.
        del self.ifd_tags[ifd_tag.tag]

    def _read_ascii_tag(self, ifd_tag):
        retval_chars = []
        cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE

        # Subtract 1 from IFD member count to ignore null terminator character.
        for member_index in range(ifd_tag.count - 1):  # pylint: disable=unused-variable
            current_ascii_val = self.segment_hex[cursor:cursor + 1 * HEX_PER_BYTE]
            retval_chars.append(chr(int(current_ascii_val, 16)))
            cursor += 1 * HEX_PER_BYTE

        return ''.join(retval_chars)

    def _read_ifd_tag(self, ifd_tag):
        # Handle strings differently, since count refers to how many letters.
        if ifd_tag.dtype == ExifTypes.ASCII:
            retval = self._read_ascii_tag(ifd_tag)
        else:
            retval = self._read_numeric_tag(ifd_tag)

        return retval

    def _read_numeric_tag(self, ifd_tag):
        retvals = []
        cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
        for member_index in range(ifd_tag.count):  # pylint: disable=unused-variable
            # If type is 4-byte or less, value is stored in member (1, 3, 4, 9).
            if ifd_tag.dtype == ExifTypes.BYTE:
                value_bits = struct.pack(ifd_tag.endian_prefix + 'I', ifd_tag.value_offset)
                retvals.append(struct.unpack(ifd_tag.endian_prefix + 'BBBB', value_bits)[0])
            elif ifd_tag.dtype == ExifTypes.SHORT:
                value_bits = struct.pack(ifd_tag.endian_prefix + 'I', ifd_tag.value_offset)
                retvals.append(struct.unpack(ifd_tag.endian_prefix + 'HH', value_bits)[0])
            elif ifd_tag.dtype == ExifTypes.LONG:
                value_bits = struct.pack(ifd_tag.endian_prefix + 'I', ifd_tag.value_offset)
                retvals.append(struct.unpack(ifd_tag.endian_prefix + 'L', value_bits)[0])
            elif ifd_tag.dtype == ExifTypes.SLONG:
                value_bits = struct.pack(ifd_tag.endian_prefix + 'I', ifd_tag.value_offset)
                retvals.append(struct.unpack(ifd_tag.endian_prefix + 'l', value_bits)[0])

            # Otherwise, member is a pointer (2, 5, and 10).
            elif ifd_tag.dtype == ExifTypes.RATIONAL:
                data_format = ifd_tag.endian_prefix + "LL"
                numerator, denominator = struct.unpack(data_format, binascii.unhexlify(
                    self.segment_hex[cursor:cursor + 8 * HEX_PER_BYTE]))
                cursor += 8 * HEX_PER_BYTE
                retvals.append(float(numerator) / float(denominator))
            elif ifd_tag.dtype == ExifTypes.SRATIONAL:
                data_format = ifd_tag.endian_prefix + "ll"
                numerator, denominator = struct.unpack(data_format, binascii.unhexlify(
                    self.segment_hex[cursor:cursor + 8 * HEX_PER_BYTE]))
                cursor += 8 * HEX_PER_BYTE
                retvals.append(float(numerator) / float(denominator))
            else:
                raise RuntimeError("unknown datatype value")

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval

    def _modify_ascii_tag(self, ifd_tag, value):
        if len(value) > ifd_tag.count - 1:
            raise ValueError("string must be no longer than original")

        cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
        new_segment_hex = self.segment_hex[:cursor]
        for character in value:
            new_segment_hex += hex(ord(character)).lstrip('0x')
            cursor += 1 * HEX_PER_BYTE
        for _i in range(ifd_tag.count - 1 - len(value)):
            new_segment_hex += '00'
            cursor += 1 * HEX_PER_BYTE

        new_segment_hex += self.segment_hex[cursor:]
        ifd_tag.count = len(value) + 1
        self.segment_hex = new_segment_hex

    def _modify_ifd_tag(self, ifd_tag, value):
        if ifd_tag.dtype == ExifTypes.ASCII:
            self._modify_ascii_tag(ifd_tag, value)
        else:
            self._modify_numeric_tag(ifd_tag, value)

    def _modify_numeric_tag(self, ifd_tag, value):
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == ifd_tag.count
        else:
            assert ifd_tag.count == 1
            value = (value,)

        cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
        for member_index in range(ifd_tag.count):
            # If type is 4-byte or less, value is stored in member (1, 3, 4, 9).
            if ifd_tag.dtype == ExifTypes.BYTE:
                raise RuntimeError("this package does not yet support setting BYTE tags")
            elif ifd_tag.dtype == ExifTypes.SHORT:
                raise RuntimeError("this package does not yet support setting SHORT tags")
            elif ifd_tag.dtype == ExifTypes.LONG:
                raise RuntimeError("this package does not yet support setting LONG tags")
            elif ifd_tag.dtype == ExifTypes.SLONG:
                raise RuntimeError("this package does not yet support setting SLONG tags")

            # Otherwise, member is a pointer (2, 5, and 10).
            elif ifd_tag.dtype == ExifTypes.RATIONAL:
                fraction = Fraction(value[member_index]).limit_denominator()
                new_member_bits = struct.pack(
                    ifd_tag.endian_prefix + "LL", fraction.numerator, fraction.denominator)
                new_member_hex = binascii.hexlify(new_member_bits)
                if sys.version_info[0] == 3:  # pragma: no cover
                    new_member_hex = new_member_hex.decode("utf8")
                self.segment_hex = (self.segment_hex[:cursor] + new_member_hex +
                                    self.segment_hex[cursor + 8 * HEX_PER_BYTE:])
                cursor += 8 * HEX_PER_BYTE
            elif ifd_tag.dtype == ExifTypes.SRATIONAL:
                fraction = Fraction(value[member_index]).limit_denominator()
                new_member_bits = struct.pack(
                    ifd_tag.endian_prefix + "ll", fraction.numerator, fraction.denominator)
                new_member_hex = binascii.hexlify(new_member_bits)
                if sys.version_info[0] == 3:  # pragma: no cover
                    new_member_hex = new_member_hex.decode("utf8")
                self.segment_hex = (self.segment_hex[:cursor] + new_member_hex +
                                    self.segment_hex[cursor + 8 * HEX_PER_BYTE:])
                cursor += 8 * HEX_PER_BYTE

            else:
                raise RuntimeError("unknown datatype value")

    def _unpack_ifd_tags(self):
        cursor = 0xA * HEX_PER_BYTE
        exif_offset = None
        gps_offset = None

        # Read the endianness specified by the image.
        self._endianness = self.segment_hex[cursor:cursor+2*HEX_PER_BYTE]
        cursor += 2 * HEX_PER_BYTE

        # Skip over fixed 0x002A bytes.
        cursor += 2 * HEX_PER_BYTE

        # Determine the location of the first IFD section relative to the start of the APP1 section.
        first_ifd_offset = self.segment_hex[cursor:cursor + 4 * HEX_PER_BYTE]
        # 0xA is IFD section offset from start of APP1.
        cursor = (0xA + int(first_ifd_offset, 16)) * HEX_PER_BYTE

        # Read each IFD section.
        current_ifd = 0
        while cursor != 0xA*HEX_PER_BYTE:
            section_start_address = cursor
            num_ifd_tags = int(self.segment_hex[cursor:cursor+2*HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag = IfdTag(
                    self._endianness,
                    self.segment_hex[cursor:cursor + BYTES_PER_IFD_TAG * HEX_PER_BYTE],
                    section_start_address)
                self.ifd_tags[tag.tag] = tag
                if tag.is_exif_pointer():
                    exif_offset = tag.value_offset
                if tag.is_gps_pointer():
                    gps_offset = tag.value_offset
                cursor += BYTES_PER_IFD_TAG * HEX_PER_BYTE

            cursor = (0xA + int(self.segment_hex[cursor:cursor+4*HEX_PER_BYTE], 16)) * HEX_PER_BYTE
            current_ifd += 1

        # If an EXIF section pointer exists, read EXIF IFD tags.
        if exif_offset:
            cursor = (0xA + exif_offset) * HEX_PER_BYTE
            section_start_address = cursor
            num_ifd_tags = int(self.segment_hex[cursor:cursor + 2 * HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag = IfdTag(
                    self._endianness,
                    self.segment_hex[cursor:cursor + BYTES_PER_IFD_TAG * HEX_PER_BYTE],
                    section_start_address)
                self.ifd_tags[tag.tag] = tag
                cursor += BYTES_PER_IFD_TAG * HEX_PER_BYTE

        # If an GPS section pointer exists, read GPS IFD tags.
        if gps_offset:
            cursor = (0xA + gps_offset) * HEX_PER_BYTE
            section_start_address = cursor
            num_ifd_tags = int(self.segment_hex[cursor:cursor + 2 * HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for tag_index in range(num_ifd_tags):  # pylint: disable=unused-variable
                tag = IfdTag(
                    self._endianness,
                    self.segment_hex[cursor:cursor + BYTES_PER_IFD_TAG * HEX_PER_BYTE],
                    section_start_address)
                self.ifd_tags[tag.tag] = tag
                cursor += BYTES_PER_IFD_TAG * HEX_PER_BYTE

    def __init__(self, segment_hex):
        self._endianness = None
        self.segment_hex = segment_hex
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

        return self._read_ifd_tag(ifd_tag)

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

            self._modify_ifd_tag(ifd_tag, value)
