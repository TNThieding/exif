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

Alternatively, supply a file path or image bytes to the ``exif.Image`` class::

    >>> my_image = Image('grand_canyon.jpg')

    >>> from exif import Image
    >>> with open('grand_canyon.jpg', 'rb') as image_file:
    ...     image_bytes = image_file.read()
    ...
    >>> my_image = Image(image_bytes)

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

Set new attribute values to add EXIF tags to an image::

    >>> from exif import LightSource
    >>> my_image.light_source = LightSource.DAYLIGHT

Use ``del`` notation to remove EXIF tags from the image::

    >>> del my_image.gps_latitude
    >>> del my_image.gps_longitude

Indexed/Item Syntax
+++++++++++++++++++

Alternatively, use indexed/item syntax to read, modify, add, and remove attribute tags::

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

Call ``set()`` with a tag name and value to add or modify it::

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

********
Cookbook
********

Add Geolocation
+++++++++++++++

Add geolocation metadata to an image by providing tuples of degrees, minutes,
and decimal seconds::

    >>> from exif import Image
    >>> image = Image("cleveland_public_square.jpg")
    >>>
    >>> image.gps_latitude = (41.0, 29.0, 57.48)
    >>> image.gps_latitude_ref = "N"
    >>> image.gps_longitude = (81.0, 41.0, 39.84)
    >>> image.gps_longitude_ref = "W"
    >>> image.gps_altitude = 199.034  # in meters
    >>> image.gps_altitude_ref = GpsAltitudeRef.ABOVE_SEA_LEVEL
    >>>
    >>> # Then, save image to desired location using code discussed above.

Add Timestamps
++++++++++++++

Use ``datetime_original`` and ``datetime_digitized`` to add timestamps to an
image (e.g., from a scanner)::

    >>> from exif import Image, DATETIME_STR_FORMAT
    >>> from datetime import datetime
    >>> datetime_taken = datetime(year=1999, month=12, day=31, hour=23, minute=49, second=12)
    >>> datetime_scanned = datetime(year=2020, month=7, day=11, hour=10, minute=11, second=37)
    >>>
    >>> image = Image("my_scanned_photo.jpg")
    >>> image.datetime_original = datetime_taken.strftime(DATETIME_STR_FORMAT)
    >>> image.datetime_digitized = datetime_scanned.strftime(DATETIME_STR_FORMAT)
    >>> # Then, save image to desired location using code discussed above.

Use with NumPy and OpenCV Image Encoder
+++++++++++++++++++++++++++++++++++++++

*This sample script was provided by Rune Monzel.*

It demonstrates how to use this package with NumPy and an image encoder, specifically
OpenCV in this case::

    import exif
    import cv2
    import numpy as np

    # Create a random 2D array within range [0 255]
    image = (np.random.rand(800, 1200) * 255).astype(np.uint8)

    # decode to the appropriate format
    # jpg -> compressed with information loss)
    status, image_jpg_coded = cv2.imencode('.jpg', image)
    print('successful jpg encoding: %s' % status)
    # tif -> no compression, no information loss
    status, image_tif_coded = cv2.imencode('.jpg', image)
    print('successful tif encoding: %s' % status)

    # to a byte string
    image_jpg_coded_bytes = image_jpg_coded.tobytes()
    image_tif_coded_bytes = image_tif_coded.tobytes()

    # using the exif format to add information
    exif_jpg = exif.Image(image_jpg_coded_bytes)
    exif_tif = exif.Image(image_tif_coded_bytes)

    # providing some information
    user_comment = "random image"
    software = "created in python with numpy"
    author = "Rune Monzel"

    # adding information to exif files:
    exif_jpg["software"] = exif_tif["software"] = software
    exif_jpg["user_comment"] = exif_tif["user_comment"] = user_comment

    # show existing tags
    print(exif_jpg.list_all())

    # save image
    with open(r'random.tif', 'wb') as new_image_file:
        new_image_file.write(exif_tif.get_file())
    with open(r'random.jpg', 'wb') as new_image_file:
        new_image_file.write(exif_jpg.get_file())
