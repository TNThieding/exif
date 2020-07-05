"""Test adding EXIF attributes."""

import binascii
import os
import textwrap
import unittest

from exif import Image
from exif.tests.add_exif_baselines.swap_short import SWAP_SHORT_BASELINE, SWAP_SHORT_LE_BASELINE

# pylint: disable=protected-access


class TestAddExif(unittest.TestCase):

    """Test cases for adding EXIF attributes."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        florida = os.path.join(os.path.dirname(__file__), 'florida_beach.jpg')
        little_endian = os.path.join(os.path.dirname(__file__), 'little_endian.jpg')
        self.image = Image(florida)
        self.image_le = Image(little_endian)

        assert self.image.has_exif
        assert self.image_le.has_exif

    def test_swap_short(self):
        """Test deleting an existing SHORT tag to make room for a new one."""
        del self.image.subject_area
        del self.image.focal_length_in_35mm_film

        self.image.light_source = 1
        self.image.contrast = 0

        segment_hex = binascii.hexlify(self.image._segments['APP1'].get_segment_bytes()).decode("utf-8").upper()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         SWAP_SHORT_BASELINE)

    def test_swap_le_short(self):
        """Test deleting an existing SHORT tag to make room for a new one in a little endian image."""
        del self.image_le.saturation
        self.image_le.contrast = 1

        segment_hex = binascii.hexlify(self.image_le._segments['APP1'].get_segment_bytes()).decode("utf-8").upper()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         SWAP_SHORT_LE_BASELINE)
