"""Base IFD tag structure parser module."""


class Base:

    """Base IFD tag structure parser class."""

    def __init__(self, tag_offset, app1_body_bytes, endianness):
        self._tag_offset = tag_offset
        self._app1_body_bytes = app1_body_bytes
        self._endianness = endianness

    def __eq__(self, other):
        return self._tag_offset == other._tag_offset

    def __repr__(self):
        return "_ifd_tag.Base(tag_offset={})".format(self._tag_offset)

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
