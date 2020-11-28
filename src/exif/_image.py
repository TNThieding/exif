"""Image EXIF metadata interface module."""

import os
import warnings

from plum import unpack
from plum.int.big import UInt16

from exif._constants import ATTRIBUTE_ID_MAP, ExifMarkers
from exif._app1_create import generate_empty_app1_bytes
from exif._app1_metadata import App1MetaData


class Image:

    """Image EXIF metadata interface class.

    :param img_file: image file with EXIF metadata
    :type image_file: str (file path), bytes (already-read contents), or File

    """

    has_exif = None
    """Boolean reporting whether or not the image currently has EXIF metadata."""

    def _parse_segments(self, img_bytes):
        cursor = 0

        # Traverse hexadecimal string until EXIF APP1 segment found.
        while img_bytes[cursor:cursor + len(ExifMarkers.APP1)] != ExifMarkers.APP1:
            cursor += len(ExifMarkers.APP1)
            if cursor > len(img_bytes):
                self.has_exif = False
                cursor = 2  # should theoretically go after SOI marker (if adding)
                break

        self._segments['preceding'] = img_bytes[:cursor]
        app1_start_index = cursor

        if self.has_exif:
            # Determine the expected length of the APP1 segment.
            app1_len = unpack(UInt16, img_bytes[app1_start_index + 2:app1_start_index + 4])
            cursor += app1_len + 1

            # If the expected length stops early, keep traversing until another section is found.
            while img_bytes[cursor - 2:cursor - 1] != ExifMarkers.SEG_PREFIX:
                cursor += 1
                # raise IOError("no subsequent EXIF segment found, is this an EXIF-encoded JPEG?")
                if cursor > len(img_bytes):
                    self.has_exif = False
                    break

        if self.has_exif:
            # Instantiate an APP1 segment object to create an EXIF tag interface.
            self._segments['APP1'] = App1MetaData(img_bytes[app1_start_index:cursor])
            self._segments['succeeding'] = img_bytes[cursor:]
        else:
            # Store the remainder of the image so that it can be reconstructed when exporting.
            self._segments['succeeding'] = img_bytes[app1_start_index:]

    def __init__(self, img_file):
        self.has_exif = True
        self._segments = {}

        if hasattr(img_file, "read"):
            img_bytes = img_file.read()
        elif isinstance(img_file, bytes):
            img_bytes = img_file
        elif os.path.isfile(img_file):
            with open(img_file, "rb") as file_descriptor:
                img_bytes = file_descriptor.read()
        else:  # pragma: no cover
            raise ValueError("expected file object, file path as str, or bytes")

        self._parse_segments(img_bytes)

    def __dir__(self):
        members = ['delete', 'delete_all', 'get', 'get_file', 'get_thumbnail', 'has_exif', '_segments']

        if self.has_exif:
            members += self._segments['APP1'].get_tag_list()

        return members

    def __getattr__(self, item):
        return getattr(self._segments['APP1'], item)

    def __setattr__(self, key, value):
        try:
            ATTRIBUTE_ID_MAP[key.lower()]
        except KeyError:
            super(Image, self).__setattr__(key, value)
        else:
            if not self.has_exif:
                self._segments['APP1'] = App1MetaData(generate_empty_app1_bytes())
                self.has_exif = True

            setattr(self._segments['APP1'], key.lower(), value)

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
        for _ in range(2):  # iterate twice to delete thumbnail tags the second time around
            for tag in self._segments['APP1'].get_tag_list():
                try:
                    self.__delattr__(tag)
                except AttributeError:
                    warnings.warn("could not delete tag " + tag, RuntimeWarning)

            self._parse_segments(self.get_file())

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
        img_bytes = self._segments['preceding']

        if self.has_exif:
            img_bytes += self._segments['APP1'].get_segment_bytes()

        img_bytes += self._segments['succeeding']

        return img_bytes

    def get_thumbnail(self):
        """Extract thumbnail binary contained in EXIF metadata.

        :returns: thumbnail binary
        :rtype: bytes
        :raises RuntimeError: image does not contain thumbnail

        """
        try:
            app1_segment = self._segments['APP1']
        except KeyError:
            thumbnail_bytes = None
        else:
            thumbnail_bytes = app1_segment.thumbnail_bytes

        if not thumbnail_bytes:
            raise RuntimeError("image does not contain thumbnail")

        return thumbnail_bytes

    def set(self, attribute, value):
        """Set the value of the specified attribute.

        :param str attribute: image EXIF attribute name
        :param value: tag value
        :type value: corresponding Python type

        """
        self.__setattr__(attribute, value)
