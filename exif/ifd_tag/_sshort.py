"""IFD SSHORT tag structure parser module."""

from plum.int.big import SInt16
from plum.int.little import SInt16 as SInt16_L

from exif._datatypes import TiffByteOrder
from exif.ifd_tag._short import Short
from exif.ifd_tag._base import Base as BaseIfdTag


class Sshort(BaseIfdTag):

    """IFD SHORT tag structure parser class."""

    ENUMS_MAP = Short.ENUMS_MAP

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._int16_cls = SInt16
        else:
            self._int16_cls = SInt16_L

    def modify(self, value):  # pragma: no cover
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
