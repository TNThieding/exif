"""Test reading EXIF attributes."""

import os
import unittest

from baseline import Baseline

from exif import Image

# pylint: disable=pointless-statement


class TestReadExif(unittest.TestCase):

    """Test cases for reading EXIF attributes."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

    def test_get_method(self):
        """Test behavior when accessing tags using the ``get()`` method."""
        self.assertIsNone(self.image.get('fake_attribute'))
        self.assertEqual(self.image.get('light_source', default=-1), -1)  # tag not in image
        self.assertEqual(self.image.get('make'), Baseline("""Apple"""))

    def test_handle_bad_attribute(self):
        """Verify that accessing a nonexistent attribute raises an AttributeError."""
        with self.assertRaisesRegex(AttributeError, "unknown image attribute fake_attribute"):
            self.image.fake_attribute

    def test_handle_unset_attribute(self):
        """Verify that accessing an attribute not present in an image raises an AttributeError."""
        with self.assertRaisesRegex(AttributeError, "image does not have attribute light_source"):
            self.image.light_source

    def test_index_accessor(self):
        """Test accessing attributes using index syntax."""
        self.assertEqual(self.image["datetime"], Baseline("""2018:03:12 10:12:07"""))

    def test_read_ascii(self):
        """Test reading ASCII tags and compare to known baseline values."""
        self.assertEqual(self.image.datetime, Baseline("""2018:03:12 10:12:07"""))
        self.assertEqual(self.image.make, Baseline("""Apple"""))
        self.assertEqual(self.image.model, Baseline("""iPhone 7"""))

    def test_read_byte(self):
        """Test reading BYTE tags and compare to known baseline values."""
        self.assertEqual(str(self.image.gps_altitude_ref), Baseline("""0"""))

    def test_read_long(self):
        """Test reading LONG tags and compare to known baseline values."""
        self.assertEqual(str(self.image.jpeg_interchange_format), Baseline("""6410"""))
        self.assertEqual(str(self.image.jpeg_interchange_format_length), Baseline("""4507"""))

    def test_read_rational(self):
        """Test reading RATIONAL tags and compare to known baseline values."""
        self.assertEqual(str(self.image.gps_altitude)[:13], Baseline("""2189.98969072"""))
        self.assertEqual(str(self.image.gps_latitude), Baseline("""(36.0, 3.0, 11.08)"""))
        self.assertEqual(str(self.image.gps_longitude), Baseline("""(112.0, 5.0, 4.18)"""))
        self.assertEqual(str(self.image.x_resolution), Baseline("""72.0"""))
        self.assertEqual(str(self.image.y_resolution), Baseline("""72.0"""))

    def test_read_short(self):
        """Test reading a SHORT tag and compare to a known baseline value."""
        self.assertEqual(str(self.image.metering_mode), Baseline("""5"""))

    def test_read_srational(self):
        """Test reading a SRATIONAL tag and compare to a known baseline value."""
        self.assertEqual(str(self.image.brightness_value)[:13], Baseline("""11.3644957983"""))
