"""Test modifying EXIF attributes."""

import os
import unittest

from baseline import Baseline

from exif import Image


class TestModifyExif(unittest.TestCase):

    def setUp(self):
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

    def test_handle_unset_attribute(self):
        with self.assertRaisesRegexp(AttributeError, "image does not have attribute light_source"):
            self.image.light_source = 0

    def test_handle_ascii_too_long(self):
        with self.assertRaisesRegexp(ValueError, "string must be no longer than original"):
            self.image.model = "MyArtificiallySetCameraAttribute"

    def test_modify_ascii_same_len(self):
        self.image.model = "MyCamera"
        self.assertEqual(self.image.model, Baseline("""MyCamera"""))

    def test_modify_ascii_shorter(self):
        self.image.model = "MyCam"
        self.assertEqual(self.image.model, Baseline("""MyCam"""))

    def test_modify_rational(self):
        self.image.gps_altitude = 123.456789
        self.assertEqual(str(self.image.gps_altitude), Baseline("""123.456789"""))
        self.image.gps_latitude = (41.0, 36.0, 33.786)
        self.assertEqual(str(self.image.gps_latitude), Baseline("""(41.0, 36.0, 33.786)"""))

    def test_modify_srational(self):
        self.image.brightness_value = -2.468
        self.assertEqual(str(self.image.brightness_value), Baseline("""-2.468"""))
