"""Test special behavior for accessing Windows XP style EXIF attribute."""

import os
import unittest

from baseline import Baseline

from exif import Image


class TestWindowsXp(unittest.TestCase):

    """Test special behavior for accessing Windows XP style EXIF attribute."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        image_path = os.path.join(os.path.dirname(__file__), 'windows_xp_tags.jpg')
        with open(image_path, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_xp_author(self):
        """Test reading Windows XP author attribute."""
        self.assertEqual(self.image.xp_author, Baseline("""XP-Style Author"""))

    def test_xp_comment(self):
        """Test reading Windows XP comment attribute."""
        self.assertEqual(self.image.xp_comment, Baseline("""XP-Style Comment"""))

    def test_xp_keywords(self):
        """Test reading Windows XP author attribute."""
        self.assertEqual(self.image.xp_keywords, Baseline("""XP-Style Keywords"""))

    def test_xp_subject(self):
        """Test reading Windows XP author attribute."""
        self.assertEqual(self.image.xp_subject, Baseline("""XP-Style Subject"""))

    def test_xp_title(self):
        """Test reading Windows XP title attribute."""
        self.assertEqual(self.image.xp_title, Baseline("""XP-Style Title"""))
