"""Test special behavior for accessing Windows XP style EXIF attribute."""

import os

import pytest

from exif import Image

read_attributes = [
    ("xp_author", "XP-Style Author"),
    ("xp_comment", "XP-Style Comment"),
    ("xp_keywords", "XP-Style Keywords"),
    ("xp_subject", "XP-Style Subject"),
    ("xp_title", "XP-Style Title"),
]


@pytest.mark.parametrize("attribute, value", read_attributes, ids=[params[0] for params in read_attributes])
def test_read(attribute, value):
    """Test reading tags and compare to known baseline values."""
    with open(os.path.join(os.path.dirname(__file__), 'windows_xp_tags.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert getattr(image, attribute) == value
