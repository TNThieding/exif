"""Test special behavior for accessing user comment EXIF attribute."""

import binascii
import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image
from exif.tests.modify_exif_baselines import MODIFY_USER_COMMENT_BASELINE


class TestUserComment(unittest.TestCase):

    """Test special behavior for accessing user comment EXIF attribute."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        image_path = os.path.join(os.path.dirname(__file__), 'user_comment.jpg')
        with open(image_path, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_modify_ascii_same_len(self):
        """Verify that writing a same length string to an ASCII tag updates the tag."""
        # pylint: disable=protected-access
        self.image.user_comment = "Updated user comment."
        self.assertEqual(self.image.user_comment, Baseline("""Updated user comment."""))

        segment_hex = binascii.hexlify(self.image._segments['APP1'].get_segment_bytes()).decode("utf-8").upper()
        self.assertEqual('\n'.join(textwrap.wrap(segment_hex, 90)),
                         MODIFY_USER_COMMENT_BASELINE)

    def test_handle_ascii_too_long(self):
        """Verify that writing a longer string to an ASCII tag raises a ValueError."""
        with self.assertRaisesRegex(ValueError, "comment must be no longer than original"):
            self.image.user_comment = ("This image shall be used in a package regression/unit test to verify reading "
                                       "this user comment attribute which I'm making longer by adding this extra text.")

    def test_read(self):
        """Test reading a user comment."""
        self.assertEqual(
            self.image.user_comment,
            "This image shall be used in a package regression/unit test to verify reading this "
            "user comment attribute."
        )
