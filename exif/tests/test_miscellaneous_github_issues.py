"""Regression test for miscellaneous GitHub issues.."""

import os
import unittest

from baseline import Baseline

from exif import Image

# pylint: disable=pointless-statement


class TestGitHubIssue12(unittest.TestCase):

    """Regression test for GitHub issue 12."""

    def setUp(self):
        """Open sample image file in binary mode for use in test cases."""
        test_image_path = os.path.join(os.path.dirname(__file__), 'github_issue_12.jpg')
        with open(test_image_path, 'rb') as image_file:
            self.image = Image(image_file)

        assert self.image.has_exif

    def test_get_method(self):
        """Test reading ASCII tags whose values fit inside the value offset field such that it's not a pointer."""
        self.assertEqual(self.image.image_description, Baseline("""dav"""))
        self.image.image_description = "new"
        self.assertEqual(self.image.image_description, Baseline("""new"""))
