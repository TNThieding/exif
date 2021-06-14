"""Legacy Windows XP style tag structure parser module."""

from plum.dump import Record
from plum.utilities import getbytes

from exif.ifd_tag._base import Base as BaseIfdTag


class WindowsXp(BaseIfdTag):

    """Legacy Windows XP style tag structure parser class."""

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError(
            "this package does not yet support setting Windows XP style tags"
        )

    def read(self):
        """Read tag value.

        In string types, the count refers to how many characters exist in the string. In Windows XP type tags, every
        other byte is null for some reason, so skip over them.

        :returns: tag value
        :rtype: corresponding Python type

        """
        dereferenced_bytes, _ = getbytes(
            buffer=self._app1_ref.body_bytes,
            offset=int(self.tag_view.value_offset),
            dump=Record(),
            nbytes=int(self.tag_view.value_count),
        )

        cursor = 0
        ascii_string = ""

        for byte in dereferenced_bytes[
            :-2
        ]:  # discard final null termination bytes (2 for Windows XP tags)
            if (
                cursor % 2 == 0
            ):  # is at an even position and is therefore part of the string
                ascii_string += chr(byte)

            cursor += 1

        return ascii_string
