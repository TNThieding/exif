"""Test modifying EXIF attributes and getting new file contents."""

import binascii
import os
import sys
import textwrap
import unittest

from exif import Image
from exif.tests.get_file_baselines import GRAND_CANYON_THUMBNAIL, MODIFIED_NOISE_FILE_HEX_BASELINE


class TestGetFile(unittest.TestCase):

    """Test cases for modifying EXIF attributes and getting new file contents."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        noise = os.path.join(os.path.dirname(__file__), 'noise.jpg')
        with open(noise, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_get_file(self):
        """Verify that an image is writable to a file after modifying its EXIF metadata.

        Assert the produced file is equivalent to a known baseline.

        """
        self.image.software = "Python"
        file_hex = binascii.hexlify(self.image.get_file())
        if sys.version_info[0] == 3:
            file_hex = file_hex.decode("utf8")
        self.assertEqual('\n'.join(textwrap.wrap(file_hex, 90)), MODIFIED_NOISE_FILE_HEX_BASELINE)


def test_get_thumbnail():
    """Test file contents of thumbnail image."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    file_hex = binascii.hexlify(image.get_thumbnail()).decode("utf8")
    assert '\n'.join(textwrap.wrap(file_hex, 90)) == GRAND_CANYON_THUMBNAIL
