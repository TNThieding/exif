"""IFD LONG tag structure parser module."""

import struct

from exif._ifd_tag._base import Base as BaseIfdTag


class Long(BaseIfdTag):

    """IFD LONG tag structure parser class."""

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise RuntimeError("this package does not yet support setting LONG tags")

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []

        for member_index in range(self.count):  # pylint: disable=unused-variable
            value_bits = struct.pack('>I', self.value_offset)
            retvals.append(struct.unpack('>L', value_bits)[self.struct_index])

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval
