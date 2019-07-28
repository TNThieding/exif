"""IFD BYTE tag structure parser module."""

import struct

from exif._ifd_tag._base import Base as BaseIfdTag


class Byte(BaseIfdTag):

    """IFD BYTE tag structure parser class."""

    def modify(self, value):  # pragma: no cover
        raise NotImplementedError("this package does not yet support setting BYTE tags")

    def read(self):
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retvals = []

        for member_index in range(self.count):  # pylint: disable=unused-variable
            value_bits = struct.pack('>I', self.value_offset)
            retvals.append(struct.unpack('>BBBB', value_bits)[self.struct_index])

        if len(retvals) == 1:
            retval = retvals[0]
        else:
            retval = tuple(retvals)

        return retval
