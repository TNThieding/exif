"""IFD SHORT tag structure parser module."""

import binascii
import struct

from plum import unpack_from
from plum.int.big import UInt16
from plum.int.little import UInt16 as UInt16_L

from exif._constants import (
    ATTRIBUTE_ID_MAP, ColorSpace, EXIF_LITTLE_ENDIAN_HEADER, ExposureMode, ExposureProgram, MeteringMode, Orientation,
    ResolutionUnit, Saturation, SceneCaptureType, SensingMethod, Sharpness, WhiteBalance)
from exif._datatypes import IfdTag, IfdTag_L, TiffByteOrder
from exif._ifd_tag._base import Base as BaseIfdTag


class Short(BaseIfdTag):

    """IFD SHORT tag structure parser class."""

    ENUMS_MAP = {
        ATTRIBUTE_ID_MAP["color_space"]: ColorSpace,
        ATTRIBUTE_ID_MAP["exposure_mode"]: ExposureMode,
        ATTRIBUTE_ID_MAP["exposure_program"]: ExposureProgram,
        ATTRIBUTE_ID_MAP["metering_mode"]: MeteringMode,
        ATTRIBUTE_ID_MAP["orientation"]: Orientation,
        ATTRIBUTE_ID_MAP["resolution_unit"]: ResolutionUnit,
        ATTRIBUTE_ID_MAP["saturation"]: Saturation,
        ATTRIBUTE_ID_MAP["scene_capture_type"]: SceneCaptureType,
        ATTRIBUTE_ID_MAP["sensing_method"]: SensingMethod,
        ATTRIBUTE_ID_MAP["sharpness"]: Sharpness,
        ATTRIBUTE_ID_MAP["white_balance"]: WhiteBalance,
    }

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

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SHORT type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        if self._endianness == TiffByteOrder.BIG:
            ifd_tag_cls = IfdTag
            uint16_cls = UInt16
        else:
            ifd_tag_cls = IfdTag_L
            uint16_cls = UInt16_L

        tag_view = ifd_tag_cls.view(self._app1_body_bytes, self._tag_offset)
        retval = int(unpack_from(uint16_cls, tag_view.value_offset.pack()))

        if int(tag_view.tag_id) in self.ENUMS_MAP:
            retval = self.ENUMS_MAP[int(tag_view.tag_id)](retval)

        return retval
