import binascii
import sys

from exif._constants import ATTRIBUTE_ID_MAP, ExifMarkers, HEX_PER_BYTE
from exif._app1_metadata import App1MetaData


class Image(object):

    """Image EXIF metadata interface.

    :param file img_file: image file with EXIF metadata

    """

    def _parse_segments(self, img_hex):
        cursor = 0

        # Traverse hexadecimal string until EXIF APP1 segment found.
        while img_hex[cursor:cursor+4] != ExifMarkers.APP1:
            cursor += HEX_PER_BYTE
            if cursor > len(img_hex):
                raise RuntimeError("EXIF APP1 segment not found")
        self._segments['preceding'] = img_hex[:cursor]

        # Instantiate an App1 segment object.
        app1_len = int(img_hex[cursor+2*HEX_PER_BYTE:cursor+4*HEX_PER_BYTE], 16)
        self._segments['APP1'] = App1MetaData(img_hex[cursor:cursor + app1_len * HEX_PER_BYTE])
        cursor += app1_len*HEX_PER_BYTE

        # Store the remainder of the image.
        self._segments['succeeding'] = img_hex[cursor:]

    def __init__(self, img_file):
        self._segments = {}

        img_hex = binascii.hexlify(img_file.read()).upper()
        if sys.version_info[0] == 3:  # pragma: no cover
            img_hex = img_hex.decode("utf8")

        self._parse_segments(img_hex)

    def __getattr__(self, item):
        return getattr(self._segments['APP1'], item)

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
        img_hex = self._segments['preceding'] + self._segments['APP1'].segment_hex + self._segments['succeeding']
        return binascii.unhexlify(img_hex)
