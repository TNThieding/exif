"""Package constants."""
# pylint: disable=too-few-public-methods

from enum import IntEnum


class ColorSpace(IntEnum):
    """Color space specifier."""

    SRGB = 1
    "sRBG"

    UNCALIBRATED = 0xFFFF
    "Uncalibrated or Other"


class ExifMarkers(object):
    """EXIF marker segments bytes."""

    SEG_PREFIX = "FF"
    """Generic Segment Prefix"""

    SOI = "FFD8"
    """Start of Image"""

    APP1 = "FFE1"
    """EXIF Attribute Information (Application Segment 1)"""

    APP2 = "FFE2"
    """EXIF Extended Data (Application Segment 2)"""

    DQT = "FFDB"
    """Quantization Table Definition"""

    DHT = "FFC4"
    """Huffman Table Definition"""

    DRI = "FFDD"
    """Restart Interoperability Definition"""

    SOF = "FFC0"
    """Start of Frame"""

    SOS = "FFDA"
    """Start of Scan"""

    EOI = "FFD9"
    """End of Image"""


class ExifTypes(IntEnum):
    """EXIF datatype indicator for IFD structure."""

    BYTE = 1
    """8-Bit Unsigned Integer"""

    ASCII = 2
    """Null-Terminated ASCII Codes"""

    SHORT = 3
    """16-Bit Unsigned Integer"""

    LONG = 4
    """32-Bit Unsigned Integer"""

    RATIONAL = 5
    """Two (Numerator and Denominator) LONGs"""

    SLONG = 9
    """32-Bit Signed Integer"""

    SRATIONAL = 10
    """Two (Numerator and Denominator) SLONGs"""


class Saturation(IntEnum):
    """Saturation processing applied by camera."""

    NORMAL = 0
    """Normal Saturation"""

    LOW = 1
    """Low Saturation"""

    HIGH = 2
    """High Saturation"""


class Sharpness(IntEnum):
    """Sharpness processing applied by camera."""

    NORMAL = 0
    """Normal"""

    SOFT = 1
    """Soft"""

    HARD = 2
    """Hard"""


ATTRIBUTE_ID_MAP = {
    # TIFF Rev. 6.0 Section A: Image Data Structure Tags
    "image_width": 256,
    "image_height": 257,
    "bits_per_sample": 258,
    "compression": 259,
    "photometric_interpretation": 262,
    "orientation": 274,
    "samples_per_pixel": 277,
    "planar_configuration": 284,
    "subsampling_ratio_of_y_to_c": 530,
    "y_and_c_positioning": 531,
    "x_resolution": 282,
    "y_resolution": 283,
    "resolution_unit": 296,
    # TIFF Rev. 6.0 Section B: Recording Offset Tags
    "strip_offsets": 273,
    "rows_per_strip": 278,
    "strip_byte_counts": 279,
    "jpeg_interchange_format": 513,
    "jpeg_interchange_format_length": 514,
    # TIFF Rev. 6.0 Section C: Image Data Characteristic Tags
    "transfer_function": 301,
    "white_point": 318,
    "primary_chromaticities": 319,
    "matrix_coefficients": 529,
    "reference_black_white": 532,
    # TIFF Rev. 6.0 Section D: Other Tags
    "datetime": 306,
    "image_description": 270,
    "make": 271,
    "model": 272,
    "software": 305,
    "artist": 315,
    "copyright": 33432,
    # EXIF Tags
    "exposure_time": 33434,
    "f_number": 33437,
    "exposure_program": 34850,
    "spectral_sensitivity": 34852,
    "photographic_sensitivity": 34855,
    "oecf": 34856,
    "sensitivity_type": 34864,
    "standard_output_sensitivity": 34865,
    "recommended_exposure_index": 34866,
    "iso_speed": 34867,
    "iso_speed_latitude_yyy": 34868,
    "iso_speed_latitude_zzz": 34869,
    "exif_version": 36864,
    "datetime_original": 36867,
    "datetime_digitized": 36868,
    "offset_time": 36880,
    "offset_time_original": 36880,
    "offset_time_digitized": 36881,
    "components_configuration": 37121,
    "compressed_bits_per_pixel": 37122,
    "shutter_speed_value": 37377,
    "aperture_value": 37378,
    "brightness_value": 37379,
    "exposure_bias_value": 37380,
    "max_aperture_value": 37381,
    "subject_distance": 37382,
    "metering_mode": 37383,
    "light_source": 37384,
    "flash": 37385,
    "focal_length": 37386,
    "subject_area": 37396,
    "maker_note": 37500,
    "user_comment": 37510,
    "subsec_time": 37520,
    "subsec_time_original": 37521,
    "subsec_time_digitized": 37522,
    "temperature": 37888,
    "humidity": 37889,
    "pressure": 37890,
    "water_depth": 37891,
    "acceleration": 37892,
    "camera_elevation_angle": 37893,
    "flashpix_version": 40960,
    "color_space": 40961,
    "pixel_x_dimension": 40962,
    "pixel_y_dimension": 40963,
    "related_sound_file": 40964,
    "flash_energy": 41483,
    "spatial_frequency_response": 41484,
    "focal_plane_x_resolution": 41486,
    "focal_plane_y_resolution": 41487,
    "focal_plane_resolution_unit": 41488,
    "subject_location": 41492,
    "exposure_index": 41493,
    "sensing_method": 41495,
    "file_source": 41728,
    "scene_type": 41729,
    "cfa_pattern": 41730,
    "custom_rendered": 41985,
    "exposure_mode": 41986,
    "white_balance": 41987,
    "digital_zoom_ratio": 41988,
    "focal_length_in_35mm_film": 41989,
    "scene_capture_type": 41990,
    "gain_control": 41991,
    "contrast": 41992,
    "saturation": 41993,
    "sharpness": 41994,
    "device_setting_description": 41995,
    "subject_distance_range": 41996,
    "image_unique_id": 42016,
    "camera_owner_name": 42032,
    "body_serial_number": 42033,
    "lens_specification": 42034,
    "lens_make": 42035,
    "lens_model": 42036,
    "lens_serial_number": 42037,
    "gamma": 42240,
    # GPS Info Tags
    "gps_version_id": 0,
    "gps_latitude_ref": 1,
    "gps_latitude": 2,
    "gps_longitude_ref": 3,
    "gps_longitude": 4,
    "gps_altitude_ref": 5,
    "gps_altitude": 6,
    "gps_timestamp": 7,
    "gps_satellites": 8,
    "gps_status": 9,
    "gps_measure_mode": 10,
    "gps_dop": 11,
    "gps_speed_ref": 12,
    "gps_speed": 13,
    "gps_track_ref": 14,
    "gps_track": 15,
    "gps_img_direction_ref": 16,
    "gps_img_direction": 17,
    "gps_map_datum": 18,
    "gps_dest_latitude_ref": 19,
    "gps_dest_latitude": 20,
    "gps_dest_longitude_ref": 21,
    "gps_dest_longitude": 22,
    "gps_dest_bearing_ref": 23,
    "gps_dest_bearing": 24,
    "gps_dest_distance_ref": 25,
    "gps_dest_distance": 26,
    "gps_processing_method": 27,
    "gps_area_information": 28,
    "gps_datestamp": 29,
    "gps_differential": 30,
    "gps_horizontal_positioning_error": 31,
    # EXIF-specific IFDs (for __dir__ Display)
    "_exif_ifd_pointer": 34665,
    "_gps_ifd_pointer": 34853,
    "_interoperability_ifd_Pointer": 40965,
}

ATTRIBUTE_NAME_MAP = {value: key for key, value in ATTRIBUTE_ID_MAP.items()}

BYTES_PER_IFD_TAG_ID = 2

BYTES_PER_IFD_TAG_TYPE = 2

BYTES_PER_IFD_TAG_COUNT = 4

BYTES_PER_IFD_TAG_VALUE_OFFSET = 4

BYTES_PER_IFD_TAG_TOTAL = (
    BYTES_PER_IFD_TAG_ID + BYTES_PER_IFD_TAG_TYPE + BYTES_PER_IFD_TAG_COUNT +
    BYTES_PER_IFD_TAG_VALUE_OFFSET
)

ERROR_IMG_NO_ATTR = "image does not have attribute {0}"

EXIF_BIG_ENDIAN_HEADER = "4D4D"

EXIF_LITTLE_ENDIAN_HEADER = "4949"

EXIF_POINTER_TAG_ID = 34665

GPS_POINTER_TAG_ID = 34853

HEX_PER_BYTE = 2
