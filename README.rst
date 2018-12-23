######
[exif]
######

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

Access EXIF metadata using Python attribute notation::

    >>> my_image.gps_latitude
    (36.0, 3.0, 11.08)
    >>> my_image.model
    'iPhone 7'
    >>> my_image.model = "Python"

Write the image with modified EXIF metadata to an image file using ``open`` in binary
write mode::

    >>> with open('modified_image.jpg', 'wb') as new_image_file:
    ...     new_image_file.write(my_image.get_file())
    ...
