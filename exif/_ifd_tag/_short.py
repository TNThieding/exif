"""IFD SHORT tag structure parser module."""

import binascii
import struct

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

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._uint16_cls = UInt16
        else:
            self._uint16_cls = UInt16_L

    def modify(self, value):
        """Modify tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SHORT type with a count greater than 1.

        :param value: new tag value
        :type value: corresponding Python type

        """
        tag_view = self._ifd_tag_cls.view(self._app1_ref.body_bytes, self._tag_offset)
        self._uint16_cls.view(self._app1_ref.body_bytes, tag_view.value_offset.__offset__).set(value)

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SHORT type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        tag_view = self._ifd_tag_cls.view(self._app1_ref.body_bytes, self._tag_offset)
        retval = self._uint16_cls.view(self._app1_ref.body_bytes, tag_view.value_offset.__offset__).get()

        if int(tag_view.tag_id) in self.ENUMS_MAP:
            retval = self.ENUMS_MAP[int(tag_view.tag_id)](retval)

        return retval
