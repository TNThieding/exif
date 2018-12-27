"""Test deleting EXIF attributes."""

import os
import textwrap
import unittest

from exif import Image
from exif.tests.delete_exif_baselines import (
    DELETE_ASCII_TAGS_HEX_BASELINE, DELETE_GEOTAG_HEX_BASELINE)

# pylint: disable=pointless-statement, protected-access


class TestModifyExif(unittest.TestCase):

    """Test cases for deleting EXIF attributes."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

    def test_delete_ascii_tags(self):
        """Verify deleting EXIF ASCII from the Image object and the hexadecimal equivalent."""
        del self.image.make
        del self.image.model

        with self.assertRaisesRegexp(AttributeError, "image does not have attribute make"):
            self.image.make
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute model"):
            self.image.model

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)), DELETE_ASCII_TAGS_HEX_BASELINE)

    def test_delete_gps_tags(self):
        """Verify deleting EXIF geotags from the Image object and the hexadecimal equivalent."""
        del self.image.gps_latitude
        del self.image.gps_longitude
        del self.image.gps_altitude

        with self.assertRaisesRegexp(AttributeError, "image does not have attribute gps_latitude"):
            self.image.gps_latitude
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute gps_longitude"):
            self.image.gps_longitude
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute gps_altitude"):
            self.image.gps_altitude

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)), DELETE_GEOTAG_HEX_BASELINE)

    def test_handle_unset_attribute(self):
        """Verify that accessing an attribute not present in an image raises an AttributeError."""
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute light_source"):
            del self.image.light_source

    def test_standard_delete(self):
        """Verify that writing and deleting non-EXIF attributes behave normally."""
        self.image.dummy_attr = 123
        assert self.image.dummy_attr == 123
        del self.image.dummy_attr
        with self.assertRaisesRegexp(AttributeError, "unknown image attribute dummy_attr"):
            self.image.dummy_attr
