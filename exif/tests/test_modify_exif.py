"""Test modifying EXIF attributes."""

import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image
from exif.tests.modify_exif_baselines import (
    MODIFY_ASCII_SAME_LEN_HEX_BASELINE, MODIFY_ASCII_SHORTER_HEX_BASELINE,
    MODIFY_RATIONAL_HEX_BASELINE, MODIFY_SRATIONAL_HEX_BASELINE, ROTATED_GRAND_CANYON_HEX)

# pylint: disable=protected-access


class TestModifyExif(unittest.TestCase):

    """Test cases for modifying EXIF attributes."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_handle_unset_attribute(self):
        """Verify that accessing an attribute not present in an image raises an AttributeError."""
        with self.assertRaisesRegex(AttributeError, "image does not have attribute light_source"):
            self.image.light_source = 0

    def test_handle_ascii_too_long(self):
        """Verify that writing a longer string to an ASCII tag raises a ValueError."""
        with self.assertRaisesRegex(ValueError, "string must be no longer than original"):
            self.image.model = "MyArtificiallySetCameraAttribute"

    def test_index_modifier(self):
        """Test modifying attributes using index syntax."""
        self.image["model"] = "MyCamera"
        self.assertEqual(self.image.model, Baseline("""MyCamera"""))

    def test_modify_ascii_same_len(self):
        """Verify that writing a same length string to an ASCII tag updates the tag."""
        self.image.model = "MyCamera"
        self.assertEqual(self.image.model, Baseline("""MyCamera"""))

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         MODIFY_ASCII_SAME_LEN_HEX_BASELINE)

    def test_modify_ascii_shorter(self):
        """Verify that writing a shorter string to an ASCII tag updates the tag."""
        self.image.model = "MyCam"
        self.assertEqual(self.image.model, Baseline("""MyCam"""))

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         MODIFY_ASCII_SHORTER_HEX_BASELINE)

    def test_modify_orientation(self):
        """Verify that modifying the orientation (a short tag) updates the tag value as expected."""
        assert self.image.orientation == 1
        assert repr(self.image.orientation) == Baseline("""<Orientation.TOP_LEFT: 1>""")

        self.image.orientation = 6
        assert self.image.orientation == 6

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         ROTATED_GRAND_CANYON_HEX)

    def test_modify_rational(self):
        """Verify that modifying RATIONAL tags updates the tag values as expected."""
        self.image.gps_altitude = 123.456789
        self.assertEqual(str(self.image.gps_altitude), Baseline("""123.456789"""))
        self.image.gps_latitude = (41.0, 36.0, 33.786)
        self.assertEqual(str(self.image.gps_latitude), Baseline("""(41.0, 36.0, 33.786)"""))

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         MODIFY_RATIONAL_HEX_BASELINE)

    def test_modify_srational(self):
        """Verify that modifying a SRATIONAL tag updates the tag value as expected."""
        self.image.brightness_value = -2.468
        self.assertEqual(str(self.image.brightness_value), Baseline("""-2.468"""))

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         MODIFY_SRATIONAL_HEX_BASELINE)

    def test_set_method(self):
        """Test behavior when setting tags using the ``set()`` method."""
        self.image.set("model", "MyCamera")
        self.assertEqual(self.image.model, Baseline("""MyCamera"""))
