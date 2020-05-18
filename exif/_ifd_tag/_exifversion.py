"""IFD EXIF version tag structure parser module."""

from exif._ifd_tag._base import Base as BaseIfdTag


class ExifVersion(BaseIfdTag):

    """Custom ASCII tag (non-terminated) structure parser class for EXIF version tag."""

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise RuntimeError("cannot modify EXIF version")

    def read(self):
        """Read tag value.

        In string types, the count refers to how many characters exist in the string.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retval_chars = []
        for character in range(self.count):  # use count of 4, don't subtract due to lack of null termination
            current_ascii_val = self.parent_segment_hex.read(self.value_offset_addr + character, 1)
            retval_chars.append(chr(int(current_ascii_val, 16)))

        return ''.join(retval_chars)
