"""Test behavior when opening images not conforming to EXIF specification."""

import os
import unittest

from exif import Image


class TestInvalidFiles(unittest.TestCase):

    """Test behavior when opening images not conforming to EXIF specification."""

    def test_invalid_app1_segment(self):
        """Verify that an image with an invalid APP1 segment marker raises an IOError.

        In this case, an invalid APP1 segment marker occurs when the parser finds an 0xFFE1 in the
        image data itself (and hence finds no metadata/tags).

        """
        image_path = os.path.join(os.path.dirname(__file__), 'invalid_exif_app1.png')
        no_subsequent_seg_msg = "no subsequent EXIF segment found, is this an EXIF-encoded JPEG?"
        with self.assertRaisesRegex(IOError, no_subsequent_seg_msg):
            with open(image_path, 'rb') as image_file:
                Image(image_file)

    def test_no_app1_segment(self):
        """Verify that an image without an APP1 segment marker raises an IOError."""
        image_path = os.path.join(os.path.dirname(__file__), 'no_app1.png')
        with self.assertRaisesRegex(IOError, "EXIF APP1 segment not found"):
            with open(image_path, 'rb') as image_file:
                Image(image_file)
