"""Test accessing and manipulating attributes of a little endian image."""

import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image
from exif.tests.little_endian_baselines import LITTLE_ENDIAN_MODIFY_BASELINE

# pylint: disable=pointless-statement, protected-access


class TestLittleEndian(unittest.TestCase):

    """Test cases for little endian images."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        little_endian_img = os.path.join(os.path.dirname(__file__), 'little_endian.jpg')
        with open(little_endian_img, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_modify(self):
        """Verify that modifying tags updates the tag values as expected."""
        self.image.model = "Modified"
        self.assertEqual(self.image.model, "Modified")

        self.image.gps_longitude = (12.0, 34.0, 56.789)
        self.assertEqual(str(self.image.gps_longitude), Baseline("""(12.0, 34.0, 56.789)"""))

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         LITTLE_ENDIAN_MODIFY_BASELINE)

    def test_read(self):
        """Test reading tags and compare to known baseline values."""
        self.assertEqual(repr(self.image.color_space), "<ColorSpace.SRGB: 1>")
        self.assertEqual(str(self.image.datetime_original), Baseline("""2019:02:08 21:44:35"""))
        self.assertEqual(str(self.image.gps_latitude),
                         Baseline("""(79.0, 36.0, 54.804590935844615)"""))
        self.assertEqual(str(self.image.gps_longitude),
                         Baseline("""(47.0, 25.0, 34.489798675854615)"""))
        self.assertEqual(self.image.make, Baseline("""EXIF Package"""))
        self.assertEqual(self.image.model, Baseline("""Little Endian"""))
        self.assertEqual(str(self.image.resolution_unit), Baseline("""2"""))
        self.assertEqual(repr(self.image.saturation), Baseline("""<Saturation.LOW: 1>"""))
        self.assertEqual(repr(self.image.sharpness), Baseline("""<Sharpness.SOFT: 1>"""))
        self.assertEqual(str(self.image.x_resolution), Baseline("""200.0"""))
        self.assertEqual(str(self.image.y_resolution), Baseline("""200.0"""))
