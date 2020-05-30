"""Test reading EXIF attributes."""

import os

import pytest
from baseline import Baseline

from exif import Image

# pylint: disable=pointless-statement


def test_get_method():
    """Test behavior when accessing tags using the ``get()`` method."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert image.get('fake_attribute') is None
    assert image.get('light_source', default=-1) == -1  # tag not in image
    assert image.get('make') == Baseline("""Apple""")


def test_handle_bad_attribute():
    """Verify that accessing a nonexistent attribute raises an AttributeError."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    with pytest.raises(AttributeError, match="unknown image attribute fake_attribute"):
        image.fake_attribute


def test_handle_unset_attribute():
    """Verify that accessing an attribute not present in an image raises an AttributeError."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    with pytest.raises(AttributeError, match="image does not have attribute light_source"):
        image.light_source


def test_index_accessor():
    """Test accessing attributes using index syntax."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert image["datetime"] == Baseline("""2018:03:12 10:12:07""")


def rounded_str(input_object):
    return str(input_object)[:13]


read_attributes = [
    ("brightness_value", rounded_str, "11.3644957983"),
    ("datetime", str, "2018:03:12 10:12:07"),
    ("exif_version", str, "0221"),
    ("gps_altitude", rounded_str, "2189.98969072"),
    ("gps_altitude_ref", str, "0"),
    ("gps_latitude", str, "(36.0, 3.0, 11.08)"),
    ("gps_latitude_ref", str, "N"),
    ("gps_longitude", str, "(112.0, 5.0, 4.18)"),
    ("gps_longitude_ref", str, "W"),
    ("jpeg_interchange_format", str, "6410"),
    ("jpeg_interchange_format_length", str, "4507"),
    ("make", str, "Apple"),
    ("metering_mode", str, "5"),
    ("model", str, "iPhone 7"),
    ("x_resolution", str, "72.0"),
    ("y_resolution", str, "72.0"),
]


@pytest.mark.parametrize("attribute, func, value", read_attributes, ids=[params[0] for params in read_attributes])
def test_read(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert func(getattr(image, attribute)) == value
