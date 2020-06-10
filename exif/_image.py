"""Image EXIF metadata interface module."""

import binascii
import sys
import warnings

from exif._constants import ATTRIBUTE_ID_MAP, ExifMarkers, HEX_PER_BYTE
from exif._app1_metadata import App1MetaData


class Image:

    """Image EXIF metadata interface class.

    :param file img_file: image file with EXIF metadata

    """

    has_exif = None
    """Boolean reporting whether or not the image currently has EXIF metadata."""

    def _parse_segments(self, img_hex):
        cursor = 0

        # Traverse hexadecimal string until EXIF APP1 segment found.
        while img_hex[cursor:cursor + 4] != ExifMarkers.APP1:
            cursor += HEX_PER_BYTE
            if cursor > len(img_hex):
                self.has_exif = False
                break

        self._segments['preceding'] = img_hex[:cursor]
        app1_start_index = cursor

        if self.has_exif:
            # Determine the expected length of the APP1 segment.

            app1_len = int(
                img_hex[app1_start_index + 2 * HEX_PER_BYTE:app1_start_index + 4 * HEX_PER_BYTE],
                16
            )
            cursor += (app1_len + 1) * HEX_PER_BYTE

            # If the expected length stops early, keep traversing until another section is found.
            while img_hex[cursor - 4:cursor - 2] != ExifMarkers.SEG_PREFIX:
                cursor += 2
                # raise IOError("no subsequent EXIF segment found, is this an EXIF-encoded JPEG?")
                if cursor > len(img_hex):
                    self.has_exif = False
                    break

        if self.has_exif:
            # Instantiate an APP1 segment object to create an EXIF tag interface.
            self._segments['APP1'] = App1MetaData(img_hex[app1_start_index:cursor])
            self._segments['succeeding'] = img_hex[cursor:]
        else:
            # Store the remainder of the image so that it can be reconstructed when exporting.
            self._segments['succeeding'] = img_hex[app1_start_index:]

    def __init__(self, img_file):
        self.has_exif = True
        self._segments = {}

        img_hex = binascii.hexlify(img_file.read()).upper()
        if sys.version_info[0] == 3:  # pragma: no cover
            img_hex = img_hex.decode("utf8")

        self._parse_segments(img_hex)

    def __dir__(self):
        members = ['delete', 'delete_all', 'get', 'get_file', 'get_thumbnail', 'has_exif', '_segments']

        if self.has_exif:
            members += self._segments['APP1'].get_tag_list()

        return members

    def __getattr__(self, item):
        return getattr(self._segments['APP1'], item)

    def __setattr__(self, key, value):
        try:
            ATTRIBUTE_ID_MAP[key]
        except KeyError:
            super(Image, self).__setattr__(key, value)
        else:
            setattr(self._segments['APP1'], key, value)

    def __delattr__(self, item):
        try:
            ATTRIBUTE_ID_MAP[item]
        except KeyError:
            super(Image, self).__delattr__(item)
        else:
            delattr(self._segments['APP1'], item)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def delete(self, attribute):
        """Remove the specified attribute from the image.

        :param str attribute: image EXIF attribute name

        """
        self.__delattr__(attribute)

    def delete_all(self):
        """Remove all EXIF tags from the image."""
        for tag in self._segments['APP1'].get_tag_list():
            try:
                self.__delattr__(tag)
            except AttributeError:
                warnings.warn("could not delete tag " + tag, RuntimeWarning)

    def get(self, attribute, default=None):
        """Return the value of the specified attribute.

        If the attribute is not available or set, return the value specified by the ``default``
        keyword argument.

        :param str attribute: image EXIF attribute name
        :param default: return value if attribute does not exist
        :returns: tag value if present, ``default`` otherwise
        :rtype: corresponding Python type

        """
        try:
            retval = self.__getattr__(attribute)
        except (AttributeError, NotImplementedError):
            retval = default

        return retval

    def get_file(self):
        """Generate equivalent binary file contents.

        :returns: image binary with EXIF metadata
        :rtype: bytes

        """
        img_hex = self._segments['preceding']

        if self.has_exif:
            img_hex += self._segments['APP1'].get_segment_hex()

        img_hex += self._segments['succeeding']

        return binascii.unhexlify(img_hex)

    def get_thumbnail(self):
        """Extract thumbnail binary contained in EXIF metadata.

        :returns: thumbnail binary
        :rtype: bytes
        :raises RuntimeError: image does not contain thumbnail

        """
        try:
            app1_segment = self._segments['APP1']
        except KeyError:
            thumbnail_hex_string = None
        else:
            thumbnail_hex_string = app1_segment.thumbnail_hex_string

        if not thumbnail_hex_string:
            raise RuntimeError("image does not contain thumbnail")

        return binascii.unhexlify(thumbnail_hex_string)

    def set(self, attribute, value):
        """Set the value of the specified attribute.

        :param str attribute: image EXIF attribute name
        :param value: tag value
        :type value: corresponding Python type

        """
        self.__setattr__(attribute, value)
