"""IFD SHORT tag structure parser module."""

import binascii
import struct

from exif._constants import (
    ATTRIBUTE_ID_MAP, ColorSpace, EXIF_LITTLE_ENDIAN_HEADER, ExposureMode, ExposureProgram, MeteringMode, Orientation,
    ResolutionUnit, Saturation, SceneCaptureType, SensingMethod, Sharpness, WhiteBalance)
from exif._ifd_tag._base import Base as BaseIfdTag


class Short(BaseIfdTag):

    """IFD SHORT tag structure parser class."""

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        # If IFD tag contains multiple values, ensure value is a tuple of appropriate length.
        if isinstance(value, tuple):
            assert len(value) == self.count
        else:
            assert self.count == 1
            value = (value,)

        for _ in range(self.count):
            if self.parent_segment_hex.endianness == EXIF_LITTLE_ENDIAN_HEADER:
                new_member_bits = struct.pack(">HH", 0, value[0])
            else:
                new_member_bits = struct.pack(">HH", value[0], 0)

            new_member_bits = binascii.hexlify(new_member_bits)
            self.parent_segment_hex.modify_hex(self.value_offset_addr, new_member_bits)
            self.value_offset = int(new_member_bits, 16)

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []

        for member_index in range(self.count):  # pylint: disable=unused-variable
            value_bits = struct.pack('>I', self.value_offset)
            retvals.append(struct.unpack('>HH', value_bits)[self.struct_index])

        retvals_in_enum = []  # Converted to enumerations where applicable.
        for retval in retvals:
            retvals_in_enum.append(self._short_to_enum(retval))

        if len(retvals_in_enum) == 1:
            retval = retvals_in_enum[0]
        else:
            retval = tuple(retvals_in_enum)

        return retval

    def _short_to_enum(self, read_number):
        retval = read_number

        if self.tag == ATTRIBUTE_ID_MAP["color_space"]:
            retval = ColorSpace(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["exposure_mode"]:
            retval = ExposureMode(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["exposure_program"]:
            retval = ExposureProgram(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["metering_mode"]:
            retval = MeteringMode(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["orientation"]:
            retval = Orientation(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["resolution_unit"]:
            retval = ResolutionUnit(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["saturation"]:
            retval = Saturation(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["scene_capture_type"]:
            retval = SceneCaptureType(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["sensing_method"]:
            retval = SensingMethod(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["sharpness"]:
            retval = Sharpness(read_number)
        elif self.tag == ATTRIBUTE_ID_MAP["white_balance"]:
            retval = WhiteBalance(read_number)
        else:
            # No enumeration found, return in original form.
            pass

        return retval
