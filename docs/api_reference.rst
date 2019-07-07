#############
API Reference
#############

.. contents::
    :local:

.. automodule:: exif

*******
Classes
*******

Image
=====

.. autoclass:: exif.Image

    .. automethod:: exif.Image.delete
    .. automethod:: exif.Image.get
    .. automethod:: exif.Image.get_file
    .. autoattribute:: exif.Image.has_exif
    .. automethod:: exif.Image.set

************
Enumerations
************

ColorSpace
==========

.. autoclass:: exif.ColorSpace
    :members:

Orientation
===========

.. autoclass:: exif.Orientation
    :members:

Saturation
==========

.. autoclass:: exif.Saturation
    :members:

Sharpness
=========

.. autoclass:: exif.Sharpness
    :members:

****************
Image Attributes
****************

The ``exif.Image`` interface provides access to the following EXIF tags as Python attributes:

- acceleration
- aperture_value
- artist
- bits_per_sample
- body_serial_number
- brightness_value
- camera_elevation_angle
- camera_owner_name
- cfa_pattern
- color_space
- components_configuration
- compressed_bits_per_pixel
- compression
- contrast
- copyright
- custom_rendered
- datetime
- datetime_digitized
- datetime_original
- device_setting_description
- digital_zoom_ratio
- exif_version
- exposure_bias_value
- exposure_index
- exposure_mode
- exposure_program
- exposure_time
- f_number
- file_source
- flash
- flash_energy
- flashpix_version
- focal_length
- focal_length_in_35mm_film
- focal_plane_resolution_unit
- focal_plane_x_resolution
- focal_plane_y_resolution
- gain_control
- gamma
- gps_altitude
- gps_altitude_ref
- gps_area_information
- gps_datestamp
- gps_dest_bearing
- gps_dest_bearing_ref
- gps_dest_distance
- gps_dest_distance_ref
- gps_dest_latitude
- gps_dest_latitude_ref
- gps_dest_longitude
- gps_dest_longitude_ref
- gps_differential
- gps_dop
- gps_horizontal_positioning_error
- gps_img_direction
- gps_img_direction_ref
- gps_latitude
- gps_latitude_ref
- gps_longitude
- gps_longitude_ref
- gps_map_datum
- gps_measur_emode
- gps_processing_method
- gps_satellites
- gps_speed
- gps_speed_ref
- gps_status
- gps_timestamp
- gps_track
- gps_track_ref
- gps_version_id
- humidity
- image_description
- image_height
- image_unique_id
- image_width
- iso_speed
- iso_speed_latitude_yyy
- iso_speed_latitude_zzz
- jpeg_interchange_format
- jpeg_interchange_format_length
- lens_make
- lens_model
- lens_serial_number
- lens_specification
- light_source
- make
- maker_note
- matrix_coefficients
- max_aperture_value
- metering_mode
- model
- oecf
- offset_time
- offset_time_digitized
- offset_time_original
- orientation
- photographic_sensitivity
- photometric_interpretation
- pixel_x_dimension
- pixel_y_dimension
- planar_configuration
- pressure
- primary_chromaticities
- recommended_exposure_index
- reference_black_white
- related_sound_file
- resolution_unit
- rows_per_strip
- samples_per_pixel
- saturation
- scene_capture_type
- scene_type
- sensing_method
- sensitivity_type
- sharpness
- shutter_speed_value
- software
- spatial_frequency_response
- spectral_sensitivity
- standard_output_sensitivity
- strip_byte_counts
- strip_offsets
- subject_area
- subject_distance
- subject_distance_range
- subject_location
- subsampling_ratio_of_y_to_c
- subsec_time
- subsec_time_digitized
- subsec_time_original
- temperature
- transfer_function
- user_comment
- water_depth
- white_balance
- white_point
- x_resolution
- y_and_c_positioning
- y_resolution