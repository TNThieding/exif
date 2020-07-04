"""Base IFD tag structure parser module."""

from exif._datatypes import IfdTag, IfdTag_L, TiffByteOrder


class Base:

    """Base IFD tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        self._tag_offset = tag_offset
        self._app1_ref = app1_ref

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._ifd_tag_cls = IfdTag
        else:
            self._ifd_tag_cls = IfdTag_L

        self._tag_view = self._ifd_tag_cls.view(self._app1_ref.body_bytes, self._tag_offset)

    def __eq__(self, other):
        return self._tag_offset == other._tag_offset

    def __repr__(self):
        return "exif.ifd_tag.Base(tag_offset={})".format(self._tag_offset)

    def modify(self, value):  # pragma: no cover
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        raise NotImplementedError("cannot modify a base/unknown IFD tag instance")

    def read(self):  # pragma: no cover
        """Read tag value.

        :returns: tag value
        :rtype: corresponding Python type

        """
        raise NotImplementedError("cannot read a base/unknown IFD tag instance")
