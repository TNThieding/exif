"""Image EXIF metadata interface module."""

import binascii
import sys

from exif._constants import ATTRIBUTE_ID_MAP, ExifMarkers, HEX_PER_BYTE
from exif._app1_metadata import App1MetaData


class Image(object):

    """Image EXIF metadata interface class.

    :param file img_file: image file with EXIF metadata

    """

    def _parse_segments(self, img_hex):
        cursor = 0

        # Traverse hexadecimal string until EXIF APP1 segment found.
        while img_hex[cursor:cursor + 4] != ExifMarkers.APP1:
            cursor += HEX_PER_BYTE
            if cursor > len(img_hex):
                raise IOError("EXIF APP1 segment not found")
        self._segments['preceding'] = img_hex[:cursor]

        # Determine the expected length of the APP1 segment.
        app1_start_index = cursor
        app1_len = int(
            img_hex[app1_start_index + 2 * HEX_PER_BYTE:app1_start_index + 4 * HEX_PER_BYTE], 16)
        cursor += app1_len * HEX_PER_BYTE

        # If the expected length stops early, keep traversing until another section prefix is found.
        while img_hex[cursor - 2:cursor] != ExifMarkers.SEG_PREFIX:
            cursor += 2

        # Instantiate an APP1 segment object to create an EXIF tag interface.
        self._segments['APP1'] = App1MetaData(img_hex[app1_start_index:cursor])

        # Store the remainder of the image so that it can be reconstructed when exporting.
        self._segments['succeeding'] = img_hex[cursor:]

    def __init__(self, img_file):
        self._segments = {}

        img_hex = binascii.hexlify(img_file.read()).upper()
        if sys.version_info[0] == 3:  # pragma: no cover
            img_hex = img_hex.decode("utf8")

        self._parse_segments(img_hex)

    def __dir__(self):
        return ['get_file', '_segments'] + self._segments['APP1'].get_tag_list()

    def __getattr__(self, item):
        return getattr(self._segments['APP1'], item)

    def __delattr__(self, item):
        try:
            ATTRIBUTE_ID_MAP[item]
        except KeyError:
            super(Image, self).__delattr__(item)
        else:
            delattr(self._segments['APP1'], item)

    def __setattr__(self, key, value):
        try:
            ATTRIBUTE_ID_MAP[key]
        except KeyError:
            super(Image, self).__setattr__(key, value)
        else:
            setattr(self._segments['APP1'], key, value)

    def get_file(self):
        """Generate equivalent binary file contents.

        :returns: image binary with EXIF metadata
        :rtype: str (Python 2) or bytes (Python 3)

        """
        img_hex = (self._segments['preceding'] + self._segments['APP1'].get_segment_hex() +
                   self._segments['succeeding'])
        return binascii.unhexlify(img_hex)
