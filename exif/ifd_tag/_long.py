"""IFD LONG tag structure parser module."""

import struct

from exif.ifd_tag._base import Base as BaseIfdTag


class Long(BaseIfdTag):

    """IFD LONG tag structure parser class."""

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError("this package does not yet support setting LONG tags since no non-pointer LONG tags "
                                  "exist in EXIF specification")

    def read(self):
        """Read tag value.

        This method does not contain logic for unpacking multiple values since the EXIF standard (v2.2) does not list
        any IFD tags of LONG type with a count greater than 1.

        :returns: tag value
        :rtype: corresponding Python type

        """
        return self.tag_view.value_offset.get()
