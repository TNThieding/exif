"""Test behavior when opening images not conforming to EXIF specification."""

import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image


NO_APP1_PNG = Baseline("""
    b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x02\\x08\\x06\\x00\\x00\\x00r
    \\xb6\\r$\\x00\\x00\\x00\\x01sRGB\\x00\\xae\\xce\\x1c\\xe9\\x00\\x00\\x00\\x04gAMA\\x00\\x00\\xb1\\x8f\\x0b\\xf
    ca\\x05\\x00\\x00\\x00\\tpHYs\\x00\\x00\\x0e\\xc2\\x00\\x00\\x0e\\xc2\\x01\\x15(J\\x80\\x00\\x00\\x00\\x1bIDAT
    \\x18Wcx+\\xa3\\xf2\\xdf\\xde\\xe3\\xcc\\x7f\\xc6\\xff\\x9f\\x18\\xfe+\\xef\\xf7a\\x00\\x00Q\\xe5\\x08\\x9ef\\x
    ebb3\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82'
    """)


class TestInvalidFiles(unittest.TestCase):

    """Test behavior when opening images not conforming to EXIF specification."""

    def test_invalid_app1_segment(self):
        """Verify that an image with an invalid APP1 segment marker raises an IOError.

        In this case, an invalid APP1 segment marker occurs when the parser finds an 0xFFE1 in the
        image data itself (and hence finds no metadata/tags).

        """
        image_path = os.path.join(os.path.dirname(__file__), 'invalid_exif_app1.png')
        with open(image_path, 'rb') as image_file:
            my_image = Image(image_file)

        self.assertFalse(my_image.has_exif)

    def test_no_app1_segment(self):
        """Verify behavior of an image without an APP1 segment marker.

        Assert the ``has_exif`` attribute is false. Verify non-EXIF ``dir()`` list contents. Then,
        check the ``get_file()`` hexadecimal.

        """
        image_path = os.path.join(os.path.dirname(__file__), 'no_app1.png')
        with open(image_path, 'rb') as image_file:
            my_image = Image(image_file)

        self.assertFalse(my_image.has_exif)

        self.assertEqual(str(dir(my_image)), Baseline("""
            ['_segments', 'delete', 'delete_all', 'get', 'get_file', 'get_thumbnail', 'has_exif']
            """))

        self.assertEqual('\n'.join(textwrap.wrap(str(my_image.get_file()), 90)), NO_APP1_PNG)
