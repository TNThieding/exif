#############
Release Notes
#############

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
