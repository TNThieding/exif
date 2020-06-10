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


read_attributes_grand_canyon = [
    ("brightness_value", rounded_str, "11.3644957983"),
    ("color_space", repr, "<ColorSpace.UNCALIBRATED: 65535>"),
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
    ("metering_mode", repr, "<MeteringMode.PATTERN: 5>"),
    ("model", str, "iPhone 7"),
    ("orientation", repr, "<Orientation.TOP_LEFT: 1>"),
    ("resolution_unit", repr, "<ResolutionUnit.INCHES: 2>"),
    ("scene_capture_type", repr, "<SceneCaptureType.STANDARD: 0>"),
    ("sensing_method", repr, "<SensingMethod.ONE_CHIP_COLOR_AREA_SENSOR: 2>"),
    ("x_resolution", str, "72.0"),
    ("y_resolution", str, "72.0"),
]


# pylint: disable=line-too-long
@pytest.mark.parametrize("attribute, func, value", read_attributes_grand_canyon, ids=[params[0] for params in read_attributes_grand_canyon])
def test_read_grand_canyon(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert func(getattr(image, attribute)) == value


read_attributes_grayson_highlands = [
    ("aperture_value", rounded_str, "1.69599371563"),
    ("brightness_value", rounded_str, "10.8686679174"),
    ("datetime_original", str, "2018:07:19 14:45:42"),
    ("exif_version", str, "0221"),
    ("exposure_mode", repr, "<ExposureMode.AUTO_EXPOSURE: 0>"),
    ("exposure_program", repr, "<ExposureProgram.NORMAL_PROGRAM: 2>"),
    ("exposure_time", rounded_str, "0.00031298904"),
    ("f_number", str, "1.8"),
    ("focal_length", str, "3.99"),
    ("focal_length_in_35mm_film", str, "28"),
    ("metering_mode", repr, "<MeteringMode.PATTERN: 5>"),
    ("white_balance", repr, "<WhiteBalance.AUTO: 0>"),
    ("x_resolution", str, "72.0"),
    ("y_resolution", str, "72.0"),
]


# pylint: disable=line-too-long
@pytest.mark.parametrize("attribute, func, value", read_attributes_grayson_highlands, ids=[params[0] for params in read_attributes_grayson_highlands])
def test_read_grayson_highlands(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(os.path.join(os.path.dirname(__file__), 'grayson_highlands.jpg'), 'rb') as image_file:
        image = Image(image_file)

    assert func(getattr(image, attribute)) == value
