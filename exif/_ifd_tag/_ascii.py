"""IFD ASCII tag structure parser module."""

import warnings

from exif._ifd_tag._base import Base as BaseIfdTag


class Ascii(BaseIfdTag):

    """IFD ASCII tag structure parser class."""

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        if len(value) > self.count - 1:
            raise ValueError("string must be no longer than original")

        if self.count <= 4:
            self.parent_segment_hex.modify_hex(self.value_offset_addr, value.encode("ascii").hex() + "00")
        else:
            cursor = 0xA + self.value_offset

            for character in value:
                self.parent_segment_hex.modify_hex(cursor, hex(ord(character)).lstrip('0x'))
                cursor += 1
            for _i in range(self.count - 1 - len(value)):
                self.parent_segment_hex.modify_hex(cursor, '00')
                cursor += 1

        self.count = len(value) + 1

    def read(self):
        """Read tag value.

        In string types, the count refers to how many characters exist in the string.

        :returns: tag value
        :rtype: corresponding Python type

        """
        retval_chars = []

        if self.count <= 4:
            for character in range(self.count - 1):  # subtract 1 to ignore null end-of-string
                current_ascii_val = self.parent_segment_hex.read(self.value_offset_addr + character, 1)
                retval_chars.append(chr(int(current_ascii_val, 16)))

        else:  # value does not fit in 4 bytes; rather, it's a pointer
            cursor = 0xA + self.value_offset

            # Subtract 1 from IFD member count to ignore null terminator character.
            for member_index in range(self.count - 1):  # pylint: disable=unused-variable
                current_ascii_val = self.parent_segment_hex.read(cursor, 1)

                if not current_ascii_val:  # pragma: no cover
                    warnings.warn("reached end of string prematurely", RuntimeWarning)
                    break

                retval_chars.append(chr(int(current_ascii_val, 16)))
                cursor += 1

        return ''.join(retval_chars)
