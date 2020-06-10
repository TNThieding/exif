#####
Usage
#####

.. contents::
  :local:

.. warning::
    Back up your photos before using this tool! You are responsible for any unexpected data loss
    that may occur through improper use of this package.

****************
Opening an Image
****************

Open an image with EXIF metadata using the Python ``open()`` built-in function. Ensure the
binary mode flag (i.e. ``'rb'``) is set. Pass this image file object into the ``exif.Image`` class::

    >>> from exif import Image
    >>> with open('grand_canyon.jpg', 'rb') as image_file:
    ...     my_image = Image(image_file)
    ...

Verify that an image has EXIF metadata by leveraging the ``has_exif`` attribute::

    >>> my_image.has_exif
    True

**************
Accessing Tags
**************

List all tags present in an image with ``dir()``::

    >>> dir(my_image)
    ['<unknown EXIF tag 59932>', '<unknown EXIF tag 59933>', '_exif_ifd_pointer', '_gps_ifd_pointer', '_segments', 'aperture
    _value', 'brightness_value', 'color_space', 'components_configuration', 'compression', 'datetime', 'datetime_digitized',
    'datetime_original', 'exif_version', 'exposure_bias_value', 'exposure_mode', 'exposure_program', 'exposure_time', 'f_
    number', 'flash', 'flashpix_version', 'focal_length', 'focal_length_in_35mm_film', 'get', 'get_file', 'get_thumbnail',
    'gps_altitude', 'gps_altitude_ref', 'gps_datestamp', 'gps_dest_bearing', 'gps_dest_bearing_ref', 'gps_horizontal_
    positioning_error', 'gps_img_direction', 'gps_img_direction_ref', 'gps_latitude', 'gps_latitude_ref', 'gps_longitude',
    'gps_longitude_ref', 'gps_speed', 'gps_speed_ref', 'gps_timestamp', 'has_exif', 'jpeg_interchange_format', 'jpeg_
    interchange_format_length', 'lens_make', 'lens_model', 'lens_specification', 'make', 'maker_note', 'metering_mode',
    'model', 'orientation', 'photographic_sensitivity', 'pixel_x_dimension', 'pixel_y_dimension', 'resolution_unit',
    'scene_capture_type', 'scene_type', 'sensing_method', 'shutter_speed_value', 'software', 'subject_area', 'subsec_time_
    digitized', 'subsec_time_original', 'white_balance', 'x_resolution', 'y_and_c_positioning', 'y_resolution']

The ``Image`` class facilitates three different tag access paradigms. Leverage attribute syntax for
an intuitive object-oriented feel. Alternatively, leverage indexed/item syntax of additional methods
for more control.

Attribute Syntax
++++++++++++++++

Access EXIF tag values as attributes of the ``Image`` instance::

    >>> my_image.gps_latitude
    (36.0, 3.0, 11.08)
    >>> my_image.gps_longitude
    (112.0, 5.0, 4.18)
    >>> my_image.make
    'Apple'
    >>> my_image.model
    'iPhone 7'

Change the EXIF tag value by modifying the attribute value::

    >>> my_image.make = "Python"

Use ``del`` notation to remove EXIF tags from the image::

    >>> del my_image.gps_latitude
    >>> del my_image.gps_longitude

Indexed/Item Syntax
+++++++++++++++++++

Alternatively, use indexed/item syntax to read, modify, and remove attribute tags::

    >>> my_image["orientation"]
    1
    >>> my_image["software"] = "Python Script"
    >>> del my_image["maker_note"]


Methods
+++++++

Leverage the dictionary-style ``get()`` method to gracefully handle cases where attributes do not
exist::

    >>> my_image.get("color_space")
    <ColorSpace.UNCALIBRATED: 65535>
    >>> my_image.get("nonexistent_tag")
    None

Call ``set()`` with a tag name and value to modify it::

    >>> self.image.set("model", "EXIF Package")

Call ``delete()`` with a tag name to remove it from the image::

    >>> self.image.delete("datetime_original")

Erase all EXIF tags in an image using the ``delete_all()`` method::

    >>> my_image.delete_all()


************************
Writing/Saving the Image
************************

Write the image with modified EXIF metadata to an image file using ``open()`` in binary
write (i.e. ``'wb'``) mode::

    >>> with open('modified_image.jpg', 'wb') as new_image_file:
    ...     new_image_file.write(my_image.get_file())
    ...

Extract the thumbnail embedded within the EXIF data by using ``get_thumbnail()`` instead of
``get_file()``.
