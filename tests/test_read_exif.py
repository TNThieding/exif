"""Test reading EXIF attributes."""

import os
import sys

import pytest
from baseline import Baseline

from exif import Image

from ._utils import check_value

# pylint: disable=pointless-statement


def test_get_method():
    """Test behavior when accessing tags using the ``get()`` method."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    assert image.get("fake_attribute") is None
    assert image.get("light_source", default=-1) == -1  # tag not in image
    assert image.get("make") == Baseline("""Apple""")


def test_handle_bad_attribute():
    """Verify that accessing a nonexistent attribute raises an AttributeError."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    with pytest.raises(AttributeError, match="unknown image attribute fake_attribute"):
        image.fake_attribute


def test_handle_unset_attribute():
    """Verify that accessing an attribute not present in an image raises an AttributeError."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    with pytest.raises(
        AttributeError, match="image does not have attribute light_source"
    ):
        image.light_source


def test_index_accessor():
    """Test accessing attributes using index syntax."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    assert image["datetime"] == Baseline("""2018:03:12 10:12:07""")


def rounded_str(input_object):
    """Trim string for consistency across test environments.

    :param Object input_object: input value
    :returns: rounded string
    :rtype: str

    """
    return str(input_object)[:13]


read_attributes_grand_canyon = [
    ("brightness_value", rounded_str, "11.3644957983"),
    ("color_space", repr, "<ColorSpace.UNCALIBRATED: 65535>"),
    ("datetime", str, "2018:03:12 10:12:07"),
    ("exif_version", str, "0221"),
    ("gps_altitude", rounded_str, "2189.98969072"),
    ("gps_altitude_ref", repr, "<GpsAltitudeRef.ABOVE_SEA_LEVEL: 0>"),
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

# FUTURE: Remove this temporary 3.10 workaround after fix for https://gitlab.com/dangass/plum/-/issues/129 is available.
if not (sys.version_info.major == 3 and sys.version_info.minor == 10):
    read_attributes_grand_canyon.append(
        (
            "flash",
            str,
            "Flash(flash_fired=False, flash_return=FlashReturn.NO_STROBE_RETURN_DETECTION_FUNCTION, "
            "flash_mode=FlashMode.COMPULSORY_FLASH_SUPPRESSION, flash_function_not_present=False, "
            "red_eye_reduction_supported=False, reserved=0)",
        )
    )


# pylint: disable=line-too-long
@pytest.mark.parametrize(
    "attribute, func, value",
    read_attributes_grand_canyon,
    ids=[params[0] for params in read_attributes_grand_canyon],
)
def test_read_file_object(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    assert check_value(func(getattr(image, attribute)), value)


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
@pytest.mark.parametrize(
    "attribute, func, value",
    read_attributes_grayson_highlands,
    ids=[params[0] for params in read_attributes_grayson_highlands],
)
def test_read_file_path(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    image = Image(os.path.join(os.path.dirname(__file__), "grayson_highlands.jpg"))
    assert check_value(func(getattr(image, attribute)), value)


read_attributes_florida_beach = [
    ("aperture_value", rounded_str, "1.69599381283"),
    ("brightness_value", rounded_str, "9.46831050228"),
    ("color_space", repr, "<ColorSpace.UNCALIBRATED: 65535>"),
    ("datetime", str, "2019:03:26 19:33:47"),
    ("gps_altitude", rounded_str, "1.02077865606"),
    ("gps_altitude_ref", repr, "<GpsAltitudeRef.ABOVE_SEA_LEVEL: 0>"),
    ("gps_version_id", str, "2"),
    ("make", str, "Apple"),
    ("metering_mode", repr, "<MeteringMode.PATTERN: 5>"),
    ("model", str, "iPhone 7"),
    ("orientation", repr, "<Orientation.TOP_LEFT: 1>"),
    ("resolution_unit", repr, "<ResolutionUnit.INCHES: 2>"),
    ("white_balance", repr, "<WhiteBalance.AUTO: 0>"),
]

# FUTURE: Remove this temporary 3.10 workaround after fix for https://gitlab.com/dangass/plum/-/issues/129 is available.
if not (sys.version_info.major == 3 and sys.version_info.minor == 10):
    read_attributes_florida_beach.append(
        (
            "flash",
            str,
            "Flash(flash_fired=False, flash_return=FlashReturn.NO_STROBE_RETURN_DETECTION_FUNCTION, "
            "flash_mode=FlashMode.AUTO_MODE, flash_function_not_present=False, "
            "red_eye_reduction_supported=False, reserved=0)",
        )
    )


# pylint: disable=line-too-long
@pytest.mark.parametrize(
    "attribute, func, value",
    read_attributes_florida_beach,
    ids=[params[0] for params in read_attributes_florida_beach],
)
def test_read_bytes(attribute, func, value):
    """Test reading tags and compare to known baseline values."""
    with open(
        os.path.join(os.path.dirname(__file__), "florida_beach.jpg"), "rb"
    ) as image_file:
        image = Image(image_file.read())

    assert check_value(func(getattr(image, attribute)), value)


@pytest.mark.parametrize(
    "attribute, func, value",
    read_attributes_florida_beach,
    ids=[params[0] for params in read_attributes_florida_beach],
)
def test_get_all_member(attribute, func, value):
    """Verify value of tags reported by ``get_all()`` method."""
    with open(
        os.path.join(os.path.dirname(__file__), "florida_beach.jpg"), "rb"
    ) as image_file:
        image = Image(image_file.read())

    assert check_value(func(image.get_all()[attribute]), value)


FLORIDA_TAG_LIST = [
    "make",
    "model",
    "orientation",
    "x_resolution",
    "y_resolution",
    "resolution_unit",
    "software",
    "datetime",
    "y_and_c_positioning",
    "_exif_ifd_pointer",
    "_gps_ifd_pointer",
    "compression",
    "jpeg_interchange_format",
    "jpeg_interchange_format_length",
    "exposure_time",
    "f_number",
    "exposure_program",
    "photographic_sensitivity",
    "exif_version",
    "datetime_original",
    "datetime_digitized",
    "components_configuration",
    "shutter_speed_value",
    "aperture_value",
    "brightness_value",
    "exposure_bias_value",
    "metering_mode",
    "flash",
    "focal_length",
    "subject_area",
    "maker_note",
    "subsec_time_original",
    "subsec_time_digitized",
    "flashpix_version",
    "color_space",
    "pixel_x_dimension",
    "pixel_y_dimension",
    "sensing_method",
    "scene_type",
    "exposure_mode",
    "white_balance",
    "focal_length_in_35mm_film",
    "scene_capture_type",
    "image_unique_id",
    "lens_specification",
    "lens_make",
    "lens_model",
    "gps_version_id",
    "gps_latitude_ref",
    "gps_latitude",
    "gps_longitude_ref",
    "gps_longitude",
    "gps_altitude_ref",
    "gps_altitude",
    "gps_timestamp",
    "gps_speed_ref",
    "gps_speed",
    "gps_img_direction_ref",
    "gps_img_direction",
    "gps_dest_bearing_ref",
    "gps_dest_bearing",
    "gps_datestamp",
    "gps_horizontal_positioning_error",
]


def test_list_all():
    """Test listing all EXIF tags in an image."""
    with open(
        os.path.join(os.path.dirname(__file__), "florida_beach.jpg"), "rb"
    ) as image_file:
        image = Image(image_file.read())

    assert image.list_all() == FLORIDA_TAG_LIST
