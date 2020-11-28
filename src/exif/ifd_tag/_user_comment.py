"""IFD user comment tag structure parser module."""

from plum import getbytes
from plum.str import Str, AsciiStr

from exif.ifd_tag._base import Base as BaseIfdTag

USER_COMMENT_CHARACTER_CODE_LEN_BYTES = 8


class UserComment(BaseIfdTag):

    """IFD ASCII tag structure parser class."""

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        if len(value) + USER_COMMENT_CHARACTER_CODE_LEN_BYTES > self.tag_view.value_count:
            raise ValueError("comment must be no longer than original")

        class IfdTagStrTarget(Str, encoding="ascii", zero_termination=True,
                              nbytes=self.tag_view.value_count - USER_COMMENT_CHARACTER_CODE_LEN_BYTES):

            """Target string datatype class sized to IFD tag's specification."""

        ascii_str_bytes = IfdTagStrTarget(value).pack()
        ascii_replace_start_index = self.tag_view.value_offset.get() + USER_COMMENT_CHARACTER_CODE_LEN_BYTES
        ascii_replace_stop_index = (ascii_replace_start_index + self.tag_view.value_count -
                                    USER_COMMENT_CHARACTER_CODE_LEN_BYTES)
        self._app1_ref.body_bytes[ascii_replace_start_index:ascii_replace_stop_index] = ascii_str_bytes

        self.tag_view.value_count = len(value) + USER_COMMENT_CHARACTER_CODE_LEN_BYTES

    def read(self):
        """Read tag value.

        Since the character code designation itself is 8 bytes, this must be a pointer and cannot exist within an IFD
        tag by itself.

        :returns: tag value
        :rtype: corresponding Python type

        """
        # The string value (not null-terminated) occurs after the character code designation. (All decodable as ASCII.)
        string_value_offset = self.tag_view.value_offset.get() + USER_COMMENT_CHARACTER_CODE_LEN_BYTES
        string_len = self.tag_view.value_count.get() - USER_COMMENT_CHARACTER_CODE_LEN_BYTES

        value_bytes, _ = getbytes(self._app1_ref.body_bytes, string_value_offset, nbytes=string_len)
        return AsciiStr.unpack(value_bytes)

    def set_character_code_to_ascii(self):
        """Set the character code header to ASCII."""
        header_replace_start_index = self.tag_view.value_offset.get()
        header_replace_stop_index = self.tag_view.value_offset.get() + USER_COMMENT_CHARACTER_CODE_LEN_BYTES
        self._app1_ref.body_bytes[header_replace_start_index:header_replace_stop_index] = b'ASCII\x00\x00\x00'
