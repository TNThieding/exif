"""IFD ASCII tag structure parser module."""

import warnings

from plum import getbytes
from plum import UnpackError
from plum.int.big import UInt32
from plum.int.little import UInt32 as UInt32_L
from plum.str import Str, AsciiStr, AsciiZeroTermStr

from exif._datatypes import TiffByteOrder
from exif.ifd_tag._base import Base as BaseIfdTag


class IntraIfdAsciiStr(Str, encoding="ascii", nbytes=4):

    """ASCII string data that fits within an IFD tag."""


class Ascii(BaseIfdTag):
    """IFD ASCII tag structure parser class."""

    def __init__(self, tag_offset, app1_ref):
        super().__init__(tag_offset, app1_ref)

        if self._app1_ref.endianness == TiffByteOrder.BIG:
            self._uint32_cls = UInt32
        else:
            self._uint32_cls = UInt32_L

    def modify(self, value):
        """Modify tag value.

        :param value: new tag value
        :type value: corresponding Python type

        """
        if len(value) > self.tag_view.value_count - 1:  # subtract 1 to account for null termination character
            raise ValueError("string must be no longer than original")

        if self.tag_view.value_count <= 4:
            ascii_str_bytes = IntraIfdAsciiStr(value).pack()
            self.tag_view.value_offset = self._uint32_cls.unpack(ascii_str_bytes)

        else:  # existing ASCII value offset is a pointer

            class IfdTagStrTarget(Str, encoding="ascii", zero_termination=True, nbytes=self.tag_view.value_count):

                """Target string datatype class sized to IFD tag's specification."""

            if len(value) < 4:  # put into IFD tag instead
                # Wipe existing value at pointer-specified offset.
                ascii_str_bytes = IfdTagStrTarget().pack()  # empty bytes
                ascii_replace_stop_index = self.tag_view.value_offset + self.tag_view.value_count
                self._app1_ref.body_bytes[self.tag_view.value_offset:ascii_replace_stop_index] = ascii_str_bytes

                # Generate intra-IFD tag bytes.
                ascii_str_bytes = IntraIfdAsciiStr(value).pack()
                self.tag_view.value_offset = self._uint32_cls.unpack(ascii_str_bytes)

            else:  # modify existing ASCII string at offset
                ascii_str_bytes = IfdTagStrTarget(value).pack()
                ascii_replace_stop_index = self.tag_view.value_offset + self.tag_view.value_count
                self._app1_ref.body_bytes[self.tag_view.value_offset:ascii_replace_stop_index] = ascii_str_bytes

        self.tag_view.value_count = len(value) + 1  # add 1 to account for null termination character

    def read(self):
        """Read tag value.

        In string types, the count refers to how many characters exist in the string.

        :returns: tag value
        :rtype: corresponding Python type

        """
        if self.tag_view.value_count <= 4:
            # Value fits into the 4 bytes within IFD tag itself.
            value_bytes, _ = getbytes(self._app1_ref.body_bytes, self.tag_view.value_offset.__offset__,
                                      nbytes=self.tag_view.value_count.get())

        else:
            # Value is too large to fit in the IFD tag itself, so it's a pointer.
            value_bytes, _ = getbytes(self._app1_ref.body_bytes, self.tag_view.value_offset.get(),
                                      nbytes=self.tag_view.value_count.get())

        try:
            unpacked_value = AsciiZeroTermStr.unpack(value_bytes)
        except UnpackError:
            value_bytes_no_null_terms = value_bytes.rstrip(b"\x00")
            excess_null_bytes_in_tag = len(value_bytes) - len(value_bytes_no_null_terms) - 1  # -1 for orig. null term.

            warnings.warn("ASCII tag contains {0} fewer bytes than specified".format(excess_null_bytes_in_tag),
                          RuntimeWarning, stacklevel=4)

            unpacked_value = AsciiStr.unpack(value_bytes_no_null_terms)

        return unpacked_value

    def wipe(self):
        """Wipe value pointer target bytes to null."""
        if self.tag_view.value_count > 4:
            start_index = self.tag_view.value_offset
            stop_index = start_index + self.tag_view.value_count
            self._app1_ref.body_bytes[start_index:stop_index] = b"\x00" * self.tag_view.value_count
