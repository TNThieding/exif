"""Test deleting EXIF attributes."""

import os
import textwrap
import unittest
from tempfile import TemporaryFile

from baseline import Baseline

from exif import Image
from exif.tests.delete_exif_baselines import (
    DELETE_ALL_HEX_BASELINE, DELETE_ASCII_TAGS_HEX_BASELINE, DELETE_GEOTAG_HEX_BASELINE)

# pylint: disable=pointless-statement, protected-access


class TestModifyExif(unittest.TestCase):

    """Test cases for deleting EXIF attributes."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        grand_canyon = os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg')
        with open(grand_canyon, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_delete_all_tags(self):
        """Verify deleting all EXIF tags from the Image object."""
        self.image.delete_all()

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)), DELETE_ALL_HEX_BASELINE)

        with TemporaryFile("w+b") as temporary_file_stream:
            temporary_file_stream.write(self.image.get_file())
            temporary_file_stream.seek(0)
            reloaded_image = Image(temporary_file_stream)

        dunder_dir_text = '\n'.join(textwrap.wrap(repr(sorted(dir(reloaded_image))), 90))
        self.assertEqual(dunder_dir_text, Baseline("""
            ['<unknown EXIF tag 59932>', '_segments', 'delete', 'delete_all', 'get', 'get_file',
            'get_thumbnail', 'has_exif', 'resolution_unit', 'x_resolution', 'y_resolution']
            """))

    def test_delete_ascii_tags(self):
        """Verify deleting EXIF ASCII from the Image object and the hexadecimal equivalent."""
        del self.image.make
        del self.image.model

        with self.assertRaisesRegex(AttributeError, "image does not have attribute make"):
            self.image.make
        with self.assertRaisesRegex(AttributeError, "image does not have attribute model"):
            self.image.model

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)), DELETE_ASCII_TAGS_HEX_BASELINE)

    def test_delete_gps_tags(self):
        """Verify deleting EXIF geotags from the Image object and the hexadecimal equivalent."""
        del self.image.gps_latitude
        del self.image.gps_longitude
        del self.image.gps_altitude

        with self.assertRaisesRegex(AttributeError, "image does not have attribute gps_latitude"):
            self.image.gps_latitude
        with self.assertRaisesRegex(AttributeError, "image does not have attribute gps_longitude"):
            self.image.gps_longitude
        with self.assertRaisesRegex(AttributeError, "image does not have attribute gps_altitude"):
            self.image.gps_altitude

        segment_hex = self.image._segments['APP1'].get_segment_hex()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)), DELETE_GEOTAG_HEX_BASELINE)

    def test_delete_method(self):
        """Test behavior when setting tags using the ``delete()`` method."""
        self.image.delete("model")

        with self.assertRaisesRegex(AttributeError, "image does not have attribute model"):
            self.image.model

    def test_handle_unset_attribute(self):
        """Verify that accessing an attribute not present in an image raises an AttributeError."""
        with self.assertRaisesRegex(AttributeError, "image does not have attribute light_source"):
            del self.image.light_source

    def test_index_deleter(self):
        """Test deleting attributes using index syntax."""
        del self.image["model"]

        with self.assertRaisesRegex(AttributeError, "image does not have attribute model"):
            self.image.model

    def test_standard_delete(self):
        """Verify that writing and deleting non-EXIF attributes behave normally."""
        self.image.dummy_attr = 123
        assert self.image.dummy_attr == 123
        del self.image.dummy_attr
        with self.assertRaisesRegex(AttributeError, "unknown image attribute dummy_attr"):
            self.image.dummy_attr
