#############
Release Notes
#############

********************************************************
[0.5.1] Mid-April 2019 buxfix/patch rollup. (2019-04-14)
********************************************************

This patch addresses the following GitHub user issues:

- Previously, instantiating ``Image`` with an image file without a valid APP1 segment caused an
  infinite loop if the APP1 segment marker was found in the hexadecimal of the image itself. Now,
  the package raises an ``IOError`` indicating that the file isn't properly EXIF-encoded. (See
  https://github.com/TNThieding/exif/issues/14 for more information.)
- Previously, accessing an image's ``user_comment`` attribute raised an exception stating the
  datatype was unknown. Now, the package parses the ``user_comment`` attribute's special data
  structure as described in the EXIF specification so that users can access its value. (See
  https://github.com/TNThieding/exif/issues/15 for more information.)

***************************************************
[0.5.0] Add index/item access support. (2019-04-13)
***************************************************

Support indexed get, set, and delete access of EXIF tags. Also, offer ``set()`` and ``delete()`` methods.

This release includes the following under-the-hood changes:

- Add minimum Pylint score check to tox configuration.
- Update usage page to describe workflow and different access paradigms.

See https://github.com/TNThieding/exif/issues/13 for more information.

******************************************
[0.4.0] Add ``get()`` method. (2019-03-16)
******************************************

Previously, this package did not offer a mechanism to return a default value when attempting to access a missing tag,
causing users to rely heavily on try-except statements. Now, the ``Image`` class offers a ``get()`` method. This method
accepts a ``default=None`` keyword argument specifying the return value if the target attribute does not exist.

See https://github.com/TNThieding/exif/issues/7 for more information.

***********************************************
[0.3.1] Fix little endian support. (2018-02-10)
***********************************************

Previously, this package did not fully support little endian EXIF metadata in images, raising ``ValueError`` exceptions.
Now, reading EXIF hexadecimal strings and values takes endianness into account.

This release includes the following under-the-hood changes:

- Move tag reading and modification functions into the IFD tag class.
- Add enumerations for color space, sharpness, and saturation as a proof-of-concept for leveraging enumerations. (More
  enumerations coming soon in a future release!)
- Improve test coverage.

See https://github.com/TNThieding/exif/issues/5 for more information.

************************************************
[0.3.0] Add attribute list support. (2018-12-26)
************************************************

Implement mechanism for listing EXIF tags in an image using ``dir()``.

This release includes the following under-the-hood changes:

- Modularize hexadecimal string interface into an internal class.
- More robust test coverage and verification of hexadecimal data.

********************************************
[0.2.0] Add tag delete support. (2018-12-25)
********************************************

Add EXIF tag deletion support via Python delete attribute notation.

*******************************************
[0.1.0] Initial alpha release. (2018-12-23)
*******************************************

Release initial alpha version of ``exif`` package with the following features:

- Support for reading EXIF tags via Python get attribute notation.
- Support for modifying existing EXIF tags via Python set attribute notation.
