import binascii
import struct
from fractions import Fraction

from exif._constants import ATTRIBUTE_ID_MAP, ExifTypes, HEX_PER_BYTE
from exif._ifd_tag import IfdTag


class App1MetaData(object):

    def _unpack_ifd_tags(self):
        cursor = 0xA * HEX_PER_BYTE

        exif_offset = None
        gps_offset = None

        endianness = self.segment_hex[cursor:cursor+2*HEX_PER_BYTE]
        cursor += 2 * HEX_PER_BYTE

        cursor += 2 * HEX_PER_BYTE  # skip over fixed 0x002A value

        first_ifd_offset = self.segment_hex[cursor:cursor+4*HEX_PER_BYTE]
        cursor = (0xA + int(first_ifd_offset, 16)) * HEX_PER_BYTE

        current_ifd = 0
        while cursor != 0xA*HEX_PER_BYTE:
            num_ifd_tags = int(self.segment_hex[cursor:cursor+2*HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for i in range(num_ifd_tags):
                tag = IfdTag(endianness, self.segment_hex[cursor:cursor+12*HEX_PER_BYTE])
                self.ifd_tags[tag.tag] = tag
                if tag.is_exif_pointer():
                    exif_offset = tag.value_offset
                if tag.is_gps_pointer():
                    gps_offset = tag.value_offset
                cursor += 12*HEX_PER_BYTE

            cursor = (0xA + int(self.segment_hex[cursor:cursor+4*HEX_PER_BYTE], 16)) * HEX_PER_BYTE
            current_ifd += 1

        if exif_offset:
            cursor = (0xA + exif_offset) * HEX_PER_BYTE
            num_ifd_tags = int(self.segment_hex[cursor:cursor+2*HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for i in range(num_ifd_tags):
                tag = IfdTag(endianness, self.segment_hex[cursor:cursor+12*HEX_PER_BYTE])
                self.ifd_tags[tag.tag] = tag
                cursor += 12*HEX_PER_BYTE

        if gps_offset:
            cursor = (0xA + gps_offset) * HEX_PER_BYTE
            num_ifd_tags = int(self.segment_hex[cursor:cursor + 2 * HEX_PER_BYTE], 16)
            cursor += 2 * HEX_PER_BYTE

            for i in range(num_ifd_tags):
                tag = IfdTag(endianness, self.segment_hex[cursor:cursor + 12 * HEX_PER_BYTE])
                self.ifd_tags[tag.tag] = tag
                cursor += 12 * HEX_PER_BYTE

    def _update_ifd_tag(self, key, value):
        attribute_id = ATTRIBUTE_ID_MAP[key]  # no try/except since __setattr__ checks for existence

        try:
            ifd_tag = self.ifd_tags[attribute_id]
        except KeyError:
            raise AttributeError("image does not have attribute {0}".format(key))

        if ifd_tag.dtype == ExifTypes.ASCII:
            if len(value) > ifd_tag.count - 1:
                raise ValueError("string must be no longer than original")

            cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
            new_segment_hex = self.segment_hex[:cursor]
            for character in value:
                new_segment_hex += hex(ord(character)).lstrip('0x')
                cursor += 1 * HEX_PER_BYTE
            for _i in range(ifd_tag.count - 1 - len(value)):
                new_segment_hex += ('00')
                cursor += 1 * HEX_PER_BYTE

            new_segment_hex += self.segment_hex[cursor:]
            ifd_tag.count = len(value) + 1
            self.segment_hex = new_segment_hex

        else:
            if isinstance(value, tuple):
                assert len(value) == ifd_tag.count
            else:
                assert ifd_tag.count == 1
                value = (value,)

            cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE
            for i in range(ifd_tag.count):
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
                    fraction = Fraction(value[i]).limit_denominator()
                    new_member_bits = struct.pack(ifd_tag.endian_prefix + "LL", fraction.numerator, fraction.denominator)
                    new_member_hex = binascii.hexlify(new_member_bits)
                    self.segment_hex = self.segment_hex[:cursor] + new_member_hex + self.segment_hex[cursor + 8 * HEX_PER_BYTE:]
                    cursor += 8 * HEX_PER_BYTE
                elif ifd_tag.dtype == ExifTypes.SRATIONAL:
                    fraction = Fraction(value[i]).limit_denominator()
                    new_member_bits = struct.pack(ifd_tag.endian_prefix + "ll", fraction.numerator, fraction.denominator)
                    new_member_hex = binascii.hexlify(new_member_bits)
                    self.segment_hex = self.segment_hex[:cursor] + new_member_hex + self.segment_hex[cursor + 8 * HEX_PER_BYTE:]
                    cursor += 8 * HEX_PER_BYTE
                else:
                    raise RuntimeError("unknown datatype value")

    def __init__(self, segment_hex):
        self.segment_hex = segment_hex
        self.ifd_tags = {}

        self._unpack_ifd_tags()

    def __getattr__(self, item):
        retvals = []

        try:
            attribute_id = ATTRIBUTE_ID_MAP[item]
        except KeyError:
            raise AttributeError("unknown image attribute {0}".format(item))

        try:
            ifd_tag = self.ifd_tags[attribute_id]
        except KeyError:
            raise AttributeError("image does not have attribute {0}".format(item))

        cursor = (0xA + ifd_tag.value_offset) * HEX_PER_BYTE

        # Handle strings differently, since count refers to how many letters.
        if ifd_tag.dtype == ExifTypes.ASCII:
            retval_chars = []
            for _i in range(ifd_tag.count - 1):  # Subtract 1 to ignore null terminator.
                current_ascii_val = self.segment_hex[cursor:cursor + 1 * HEX_PER_BYTE]
                retval_chars.append(chr(int(current_ascii_val, 16)))
                cursor += 1 * HEX_PER_BYTE
            retvals.append(''.join(retval_chars))
        else:
            for _i in range(ifd_tag.count):
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
                    format = ifd_tag.endian_prefix + "LL"
                    numerator, denominator = struct.unpack(format, binascii.unhexlify(
                        self.segment_hex[cursor:cursor + 8 * HEX_PER_BYTE]))
                    cursor += 8 * HEX_PER_BYTE
                    retvals.append(float(numerator) / float(denominator))
                elif ifd_tag.dtype == ExifTypes.SRATIONAL:
                    format = ifd_tag.endian_prefix + "ll"
                    numerator, denominator = struct.unpack(format, binascii.unhexlify(
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

    def __setattr__(self, key, value):
        try:
            attribute_id = ATTRIBUTE_ID_MAP[key]
        except KeyError:
            super(App1MetaData, self).__setattr__(key, value)
        else:
            self._update_ifd_tag(key, value)
