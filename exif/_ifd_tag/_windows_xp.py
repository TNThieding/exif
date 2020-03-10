"""Legacy Windows XP style tag structure parser module."""

import warnings

from exif._ifd_tag._base import Base as BaseIfdTag


class WindowsXp(BaseIfdTag):

    """Legacy Windows XP style tag structure parser class."""

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError("this package does not yet support setting Windows XP style tags")

    def read(self):
        """Read tag value.

        In string types, the count refers to how many characters exist in the string.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retval_chars = []
        cursor = 0xA + self.value_offset

        for member_index in range(self.count - 1):  # pylint: disable=unused-variable
            current_ascii_val = self.parent_segment_hex.read(cursor, 1)

            if not current_ascii_val:  # pragma: no cover
                warnings.warn("reached end of string prematurely", RuntimeWarning)
                break

            if current_ascii_val == "00":
                break

            retval_chars.append(chr(int(current_ascii_val, 16)))
            cursor += 2

        return ''.join(retval_chars)
