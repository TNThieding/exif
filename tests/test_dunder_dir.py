"""Test listing EXIF attributes."""

import os
import textwrap
import unittest

from baseline import Baseline

from exif import Image


class TestGetFile(unittest.TestCase):

    """Test cases for listing EXIF attributes."""

    def test_list_attributes_photo(self):
        """Verify that calling dir() on a camera photo lists the expected EXIF attributes."""
        with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
            image = Image(image_file)
        dunder_dir_text = '\n'.join(textwrap.wrap(repr(sorted(dir(image))), 90))
        self.assertEqual(dunder_dir_text, Baseline("""
            ['<unknown EXIF tag 59932>', '<unknown EXIF tag 59933>', '_exif_ifd_pointer',
            '_gps_ifd_pointer', '_segments', 'aperture_value', 'brightness_value', 'color_space',
            'components_configuration', 'compression', 'datetime', 'datetime_digitized',
            'datetime_original', 'delete', 'delete_all', 'exif_version', 'exposure_bias_value',
            'exposure_mode', 'exposure_program', 'exposure_time', 'f_number', 'flash',
            'flashpix_version', 'focal_length', 'focal_length_in_35mm_film', 'get', 'get_file',
            'get_thumbnail', 'gps_altitude', 'gps_altitude_ref', 'gps_datestamp', 'gps_dest_bearing',
            'gps_dest_bearing_ref', 'gps_horizontal_positioning_error', 'gps_img_direction',
            'gps_img_direction_ref', 'gps_latitude', 'gps_latitude_ref', 'gps_longitude',
            'gps_longitude_ref', 'gps_speed', 'gps_speed_ref', 'gps_timestamp', 'has_exif',
            'jpeg_interchange_format', 'jpeg_interchange_format_length', 'lens_make', 'lens_model',
            'lens_specification', 'make', 'maker_note', 'metering_mode', 'model', 'orientation',
            'photographic_sensitivity', 'pixel_x_dimension', 'pixel_y_dimension', 'resolution_unit',
            'scene_capture_type', 'scene_type', 'sensing_method', 'shutter_speed_value', 'software',
            'subject_area', 'subsec_time_digitized', 'subsec_time_original', 'white_balance',
            'x_resolution', 'y_and_c_positioning', 'y_resolution']
            """))

    def test_list_attributes_simple(self):
        """Verify that calling dir() on a simple image lists the expected EXIF attributes."""
        with open(os.path.join(os.path.dirname(__file__), 'noise.jpg'), 'rb') as image_file:
            image = Image(image_file)
        dunder_dir_text = '\n'.join(textwrap.wrap(repr(sorted(dir(image))), 90))
        self.assertEqual(dunder_dir_text, Baseline("""
            ['_exif_ifd_pointer', '_segments', 'color_space', 'compression', 'datetime', 'delete',
            'delete_all', 'get', 'get_file', 'get_thumbnail', 'has_exif', 'jpeg_interchange_format',
            'jpeg_interchange_format_length', 'orientation', 'pixel_x_dimension', 'pixel_y_dimension',
            'resolution_unit', 'software', 'x_resolution', 'y_resolution']
            """))
