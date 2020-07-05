"""IFD EXIF version tag structure parser module."""

from plum.str import AsciiStr

from exif.ifd_tag._base import Base as BaseIfdTag


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

        :returns: tag value
        :rtype: corresponding Python type

        """
        return AsciiStr.unpack(self.tag_view.value_offset.pack())
