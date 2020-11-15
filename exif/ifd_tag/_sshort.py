"""IFD SSHORT tag structure parser module."""

from plum.int.big import SInt16
from plum.int.little import SInt16 as SInt16_L

from exif._constants import (
    ATTRIBUTE_ID_MAP, ColorSpace, ExposureMode, ExposureProgram, LightSource, MeteringMode, Orientation, ResolutionUnit,
    Saturation, SceneCaptureType, SensingMethod, Sharpness, WhiteBalance)
from exif._datatypes import Flash, TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class Sshort(BaseIfdTag):

    """IFD SHORT tag structure parser class."""

    ENUMS_MAP = {
        ATTRIBUTE_ID_MAP["color_space"]: ColorSpace,
        ATTRIBUTE_ID_MAP["exposure_mode"]: ExposureMode,
        ATTRIBUTE_ID_MAP["exposure_program"]: ExposureProgram,
        ATTRIBUTE_ID_MAP["flash"]: Flash,
        ATTRIBUTE_ID_MAP["metering_mode"]: MeteringMode,
        ATTRIBUTE_ID_MAP["light_source"]: LightSource,
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
            self._int16_cls = SInt16
        else:
            self._int16_cls = SInt16_L

    def modify(self, value):
        """Modify tag value.


        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError("this package does not yet support setting SSHORT tags since no SSHORT tags "
                                  "exist in EXIF specification")

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of SSHORT type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retval = self._int16_cls.view(self._app1_ref.body_bytes, self.tag_view.value_offset.__offset__).get()

        if int(self.tag_view.tag_id) in self.ENUMS_MAP:
            retval = self.ENUMS_MAP[int(self.tag_view.tag_id)](retval)

        return retval
