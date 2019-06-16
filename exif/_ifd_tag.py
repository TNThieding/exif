"""IFD tag structure parser module."""

import binascii
import struct
import sys
import warnings
from fractions import Fraction

from exif._constants import (
    ATTRIBUTE_ID_MAP, ColorSpace, EXIF_LITTLE_ENDIAN_HEADER, EXIF_POINTER_TAG_ID, ExifTypes,
    GPS_POINTER_TAG_ID, Saturation, Sharpness)


class IfdTag:

    """IFD tag structure parser class."""

    def __init__(self, tag, dtype, count, value_offset, section_start_address, parent_segment_hex):
        self.tag = int(tag, 16)
        self.dtype = int(dtype, 16)
        self.count = int(count, 16)
        self.value_offset = int(value_offset, 16)
        self.section_start_address = section_start_address
        self.parent_segment_hex = parent_segment_hex

    def __eq__(self, other):
        return self.tag == other.tag

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

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        if self.dtype == ExifTypes.ASCII:
            self._modify_as_ascii(value)
        else:
            self._modify_as_numeric(value)

    def _modify_as_ascii(self, value):
        if len(value) > self.count - 1:
            raise ValueError("string must be no longer than original")

        cursor = 0xA + self.value_offset

        for character in value:
            self.parent_segment_hex.modify_hex(cursor, hex(ord(character)).lstrip('0x'))
            cursor += 1
        for _i in range(self.count - 1 - len(value)):
            self.parent_segment_hex.modify_hex(cursor, '00')
            cursor += 1

        self.count = len(value) + 1

    def _modify_as_numeric(self, value):
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == self.count
        else:
            assert self.count == 1
            value = (value,)

        cursor = 0xA + self.value_offset
        for member_index in range(self.count):
            # If type is 4-byte or less, value is stored in member (1, 3, 4, 9).
            if self.dtype == ExifTypes.BYTE:
                # FUTURE: Be sure to support little endian in setting.
                raise RuntimeError("this package does not yet support setting BYTE tags")
            elif self.dtype == ExifTypes.SHORT:
                # FUTURE: Be sure to support little endian in setting.
                raise RuntimeError("this package does not yet support setting SHORT tags")
            elif self.dtype == ExifTypes.LONG:
                # FUTURE: Be sure to support little endian in setting.
                raise RuntimeError("this package does not yet support setting LONG tags")
            elif self.dtype == ExifTypes.SLONG:  # pragma: no cover
                # No test coverage since no SLONG tags exist in EXIF specifications.
                # FUTURE: Be sure to support little endian in setting.
                raise RuntimeError("this package does not yet support setting SLONG tags")

            # Otherwise, member is a pointer (2, 5, and 10).
            elif self.dtype == ExifTypes.RATIONAL:
                fraction = Fraction(value[member_index]).limit_denominator()

                if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                    new_member_bits = struct.pack(
                        ">LL", fraction.denominator, fraction.numerator)
                else:
                    new_member_bits = struct.pack(
                        ">LL", fraction.numerator, fraction.denominator)

                new_member_hex = binascii.hexlify(new_member_bits)
                if sys.version_info[0] == 3:  # pragma: no cover
                    new_member_hex = new_member_hex.decode("utf8")
                self.parent_segment_hex.modify_hex(cursor, new_member_hex)
                cursor += 8
            elif self.dtype == ExifTypes.SRATIONAL:
                fraction = Fraction(value[member_index]).limit_denominator()

                if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                    new_member_bits = struct.pack(
                        ">ll", fraction.denominator, fraction.numerator)
                else:
                    new_member_bits = struct.pack(
                        ">ll", fraction.numerator, fraction.denominator)

                new_member_hex = binascii.hexlify(new_member_bits)
                if sys.version_info[0] == 3:  # pragma: no cover
                    new_member_hex = new_member_hex.decode("utf8")
                self.parent_segment_hex.modify_hex(cursor, new_member_hex)
                cursor += 8

            else:
                raise RuntimeError("unknown datatype value {0}".format(self.dtype))

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        # Handle strings differently, since count refers to how many letters.
        if self.dtype == ExifTypes.ASCII:
            retval = self._read_as_ascii()
        else:
            retval = self._read_as_numeric()

        return retval

    def _read_as_ascii(self):
        retval_chars = []
        cursor = 0xA + self.value_offset

        # Subtract 1 from IFD member count to ignore null terminator character.
        for member_index in range(self.count - 1):  # pylint: disable=unused-variable
            current_ascii_val = self.parent_segment_hex.read(cursor, 1)

            if not current_ascii_val:  # pragma: no cover
                warnings.warn("reached end of string prematurely", RuntimeWarning)
                break

            retval_chars.append(chr(int(current_ascii_val, 16)))
            cursor += 1

        return ''.join(retval_chars)

    def _read_as_numeric(self):
        retvals = []
        cursor = 0xA + self.value_offset

        if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
            struct_index = -1
        else:
            struct_index = 0

        for member_index in range(self.count):  # pylint: disable=unused-variable
            # If type is 4-byte or less, value is stored in member (1, 3, 4, 9).
            if self.dtype == ExifTypes.BYTE:
                value_bits = struct.pack('>I', self.value_offset)
                retvals.append(struct.unpack('>BBBB', value_bits)[struct_index])
            elif self.dtype == ExifTypes.SHORT:
                value_bits = struct.pack('>I', self.value_offset)
                retvals.append(struct.unpack('>HH', value_bits)[struct_index])
            elif self.dtype == ExifTypes.LONG:
                value_bits = struct.pack('>I', self.value_offset)
                retvals.append(struct.unpack('>L', value_bits)[struct_index])
            elif self.dtype == ExifTypes.SLONG:  # pragma: no cover
                # No test coverage since no SLONG tags exist in EXIF specifications.
                value_bits = struct.pack('>I', self.value_offset)
                retvals.append(struct.unpack('>l', value_bits)[struct_index])

            # Otherwise, member is a pointer (2, 5, and 10).
            elif self.dtype == ExifTypes.RATIONAL:
                data_format = ">LL"
                numerator, denominator = struct.unpack(data_format, binascii.unhexlify(
                    self.parent_segment_hex.read(cursor, 8)))
                cursor += 8
                if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                    retvals.append(float(denominator) / float(numerator))
                else:
                    retvals.append(float(numerator) / float(denominator))
            elif self.dtype == ExifTypes.SRATIONAL:
                data_format = ">ll"
                numerator, denominator = struct.unpack(data_format, binascii.unhexlify(
                    self.parent_segment_hex.read(cursor, 8)))
                cursor += 8
                if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                    retvals.append(float(denominator) / float(numerator))
                else:
                    retvals.append(float(numerator) / float(denominator))
            else:
                raise RuntimeError("unknown datatype value {0}".format(self.dtype))

        retvals_in_enum = []  # Converted to enumerations where applicable.
        for retval in retvals:
            retvals_in_enum.append(self._read_number_to_enum(retval))

        if len(retvals_in_enum) == 1:
            retval = retvals_in_enum[0]
        else:
            retval = tuple(retvals_in_enum)

        return retval

    def _read_number_to_enum(self, read_number):
        retval = read_number

        if self.tag == ATTRIBUTE_ID_MAP["color_space"]:
            retval = ColorSpace(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["saturation"]:
            retval = Saturation(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["sharpness"]:
            retval = Sharpness(read_number)
        else:
            # No enumeration found, return in original form.
            pass

        return retval
