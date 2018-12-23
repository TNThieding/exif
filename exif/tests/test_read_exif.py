"""Test reading EXIF attributes."""

import os
import unittest

from baseline import Baseline

from exif import Image


class TestReadExif(unittest.TestCase):

    def setUp(self):
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

    def test_handle_bad_attribute(self):
        with self.assertRaisesRegexp(AttributeError, "unknown image attribute fake_attribute"):
            self.image.fake_attribute

    def test_handle_unset_attribute(self):
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute light_source"):
            self.image.light_source

    def test_read_ascii(self):
        self.assertEqual(self.image.datetime, Baseline("""2018:03:12 10:12:07"""))
        self.assertEqual(self.image.make, Baseline("""Apple"""))
        self.assertEqual(self.image.model, Baseline("""iPhone 7"""))

    def test_read_rational(self):
        self.assertEqual(str(self.image.gps_altitude), Baseline("""2189.98969072"""))
        self.assertEqual(str(self.image.gps_latitude), Baseline("""(36.0, 3.0, 11.08)"""))
        self.assertEqual(str(self.image.gps_longitude), Baseline("""(112.0, 5.0, 4.18)"""))
        self.assertEqual(str(self.image.x_resolution), Baseline("""72.0"""))
        self.assertEqual(str(self.image.y_resolution), Baseline("""72.0"""))

    def test_read_short(self):
        self.assertEqual(str(self.image.metering_mode), Baseline("""5"""))

    def test_read_srational(self):
        self.assertEqual(str(self.image.brightness_value), Baseline("""11.3644957983"""))
