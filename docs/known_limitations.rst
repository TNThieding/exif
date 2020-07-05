#################
Known Limitations
#################

This package contains the following known limitations:

- Accessing SLONG tags is not supported (since no IFD tags in the EXIF
  specification are SLONG type).
- ASCII tags cannot be modified to a value longer than their original length.
- Adding new EXIF tags to an image is not yet supported (except SHORT).
- Dynamically expanding the image metadata regions is not yet supported. As a
  temporary workaround, users can delete non-essential or unwanted tags to free
  up space for the desired new tag.
- Modifying Windows XP tags is not supported.
