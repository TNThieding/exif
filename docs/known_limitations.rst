#################
Known Limitations
#################

This package contains the following known limitations:

- Accessing SLONG tags is not supported (since no IFD tags in the EXIF
  specification are SLONG type).
- EXIF IFDs cannot be added to images that only contain IFD 0 (and/or IFD 1).
  However, GPS IFDs can be inserted if there's a subsequent IFD 1 segment. When
  adding metadata to a previously non-APP1 image, this is not a concern since
  the package adds empty 0, EXIF, and GPS IFDs.
- In Python 3.10, this package unpacks the flash attribute as an 8-bit integer instead of a ``BitFields`` type due to an
  upstream issue with the ``plum-py`` bytes interface dependency.
- Modifying Windows XP tags is not supported.
