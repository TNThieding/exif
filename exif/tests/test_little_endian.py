"""Test accessing and manipulating attributes of a little endian image."""

import os
import textwrap

import pytest
from baseline import Baseline

from exif import Image
from exif.tests.little_endian_baselines import LITTLE_ENDIAN_MODIFY_BASELINE

# pylint: disable=pointless-statement, protected-access


def test_modify():
    """Verify that modifying tags updates the tag values as expected."""
    with open(os.path.join(os.path.dirname(__file__), 'little_endian.jpg'), 'rb') as image_file:
        image = Image(image_file)

    image.model = "Modified"
    assert image.model == "Modified"

    image.gps_longitude = (12.0, 34.0, 56.789)
    assert str(image.gps_longitude) == Baseline("""(12.0, 34.0, 56.789)""")

    segment_hex = image._segments['APP1'].get_segment_hex()
    assert '\n'.join(textwrap.wrap(segment_hex, 90)) == LITTLE_ENDIAN_MODIFY_BASELINE


read_attributes = [
    ("color_space", repr, "<ColorSpace.SRGB: 1>"),
    ("datetime_original", str, "2019:02:08 21:44:35"),
    ("gps_latitude", str, "(79.0, 36.0, 54.804590935844615)"),
    ("gps_longitude", str, "(47.0, 25.0, 34.489798675854615)"),
    ("make", str, "EXIF Package"),
    ("model", str, "Little Endian"),
    ("resolution_unit", repr, "<ResolutionUnit.INCHES: 2>"),
    ("saturation", repr, "<Saturation.LOW: 1>"),
    ("sharpness", repr, "<Sharpness.SOFT: 1>"),
    ("x_resolution", str, "200.0"),
    ("y_resolution", str, "200.0"),
]


@pytest.mark.parametrize("attribute, func, value", read_attributes, ids=[params[0] for params in read_attributes])
def test_read(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(os.path.join(os.path.dirname(__file__), 'little_endian.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert func(getattr(image, attribute)) == value
