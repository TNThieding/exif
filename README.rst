##############
[exif] Package
##############

.. image:: https://travis-ci.org/TNThieding/exif.svg?branch=master
    :target: https://travis-ci.org/TNThieding/exif

.. image:: https://coveralls.io/repos/github/TNThieding/exif/badge.svg?branch=master
    :target: https://coveralls.io/github/TNThieding/exif?branch=master

.. image:: https://readthedocs.org/projects/exif/badge/?version=latest
    :target: https://exif.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Read and modify image EXIF metadata using Python without any third-party software
dependencies. For example, batch process image metadata using a Python script.

***********
Quick Start
***********

Open an image with EXIF metadata using the Python ``open`` built-in function. Ensure the
binary mode flag is set. Pass this image file object into the ``exif.Image`` class::

    >>> from exif import Image
    >>> with open('grand_canyon.jpg', 'rb') as image_file:
    ...     my_image = Image(image_file)
    ...

List EXIF attributes using the Python ``dir()`` builtin function::

    >>> dir(my_image)
    ['<unknown EXIF tag 59932>', '<unknown EXIF tag 59933>', '_exif_ifd_pointer', '_gps_ifd_pointer', '_segments', 'aperture
    _value', 'brightness_value', 'color_space', 'components_configuration', 'compression', 'datetime', 'datetime_digitized',
     'datetime_original', 'exif_version', 'exposure_bias_value', 'exposure_mode', 'exposure_program', 'exposure_time', 'f_nu
    mber', 'flash', 'flashpix_version', 'focal_length', 'focal_length_in_35mm_film', 'get_file', 'gps_altitude', 'gps_altitu
    de_ref', 'gps_datestamp', 'gps_dest_bearing', 'gps_dest_bearing_ref', 'gps_horizontal_positioning_error', 'gps_img_direc
    tion', 'gps_img_direction_ref', 'gps_latitude', 'gps_latitude_ref', 'gps_longitude', 'gps_longitude_ref', 'gps_speed', '
    gps_speed_ref', 'gps_timestamp', 'jpeg_interchange_format', 'jpeg_interchange_format_length', 'lens_make', 'lens_model',
     'lens_specification', 'make', 'maker_note', 'metering_mode', 'model', 'orientation', 'photographic_sensitivity', 'pixel
    _x_dimension', 'pixel_y_dimension', 'resolution_unit', 'scene_capture_type', 'scene_type', 'sensing_method', 'shutter_sp
    eed_value', 'software', 'subject_area', 'subsec_time_digitized', 'subsec_time_original', 'white_balance', 'x_resolution',
    'y_and_c_positioning', 'y_resolution']

Access EXIF metadata tags using Python attribute notation::

    >>> # Read tags with Python "get" notation.
    >>> my_image.gps_latitude
    (36.0, 3.0, 11.08)
    >>> my_image.gps_longitude
    (112.0, 5.0, 4.18)
    >>> my_image.model
    'iPhone 7'
    >>>
    >>> # Modify tags with Python "set" notation.
    >>> my_image.model = "Python"
    >>>
    >>> # Delete tags with Python "del" notation.
    >>> del my_image.gps_latitude
    >>> del my_image.gps_longitude

Write the image with modified EXIF metadata to an image file using ``open`` in binary
write mode::

    >>> with open('modified_image.jpg', 'wb') as new_image_file:
    ...     new_image_file.write(my_image.get_file())
    ...
