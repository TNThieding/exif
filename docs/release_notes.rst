#############
Release Notes
#############

**************************************************************************************************
[1.0.1] Fix ``UnpackError`` when reading ASCII tags with shorter value than expected. (2020-09-03)
**************************************************************************************************

Previously, reading an ASCII tag whose value was shorter than the specified size
(i.e., with excess trailing null bytes) resulted in a ``UnpackError``. Now, the
package returns the tag value with excess bytes stripped off. It also issues a
``RuntimeWarning`` stating the nonconformity to the EXIF standard and how many
extra bytes were found.

This patch addresses the following GitLab user issue:

* Cannot read EXIF tag containing excess trailing bytes. (https://gitlab.com/TNThieding/exif/issues/23)


****************************************************************************
[1.0.0] Support adding tags and adding EXIF to non-EXIF images. (2020-07-11)
****************************************************************************

Initial release with full support for adding new tags to images. This includes
adding EXIF tags to an image without any pre-existing metadata (e.g., a JPEG
produced by a scanner).

In addition, SHORT tags could only previously be added if pre-existing tags
were deleted to make room. Now, this code dynamically expands and re-packs
the EXIF/APP1 metadata section to facilitate adding new tags to images without
size limitations. ASCII tags can now be modified to a value longer than their
original length too.

Add enumeration for the following tag:

* GPS altitude reference

****************************************************************************
[0.12.0] Add preliminary support for adding IFD tags to images. (2020-07-05)
****************************************************************************

Support adding the following tag types:

* SHORT (except for TIFF attributes)

Add data types and enumerations for the following tags:

* Flash
* Light source

This release also addresses the following anomalous behavior:

* Previously, thumbnail IFD tags would overwrite the primary image's. Now,
  thumbnail IFD tags are only included if they are not included in the primary
  image IFD (e.g., ``jpeg_interchange_format``).
* Include thumbnail tags during deletion with ``delete_all()`` method.

.. note:: Refer to the `known limitations page <known_limitations.html>`_ for
          an up-to-date list of stipulations, limitations, and workarounds.

*************************************************************************************
[0.11.2] Overhaul internal bytes processing and drop Python 3.5 support. (2020-07-04)
*************************************************************************************

This under-the-hood change significantly simplifies and improves internal bytes
processing by using hte ``plum-py`` (pack / unpack memory) package instead of
a custom hexadecimal string interface like before. This patch also includes
minor, benign bug fixes with hexadecimal processing. These changes will
facilitate future development (e.g., support for adding new tags to images).

Since the ``plum-py`` package only supports Python 3.6 and higher, this version
drops support for Python 3.5.

*******************************************************************************
[0.11.1] Accept file paths and bytes when instantiating ``Image``. (2020-06-30)
*******************************************************************************

In addition to accepting an image file descriptor, also support instantiating ``Image``
with file paths or bytes (e.g., already-read files).

Part of this release contains changes submitted via GitHub pull request by the following user:

* chbndrhnns

**************************************************
[0.11.0] Add ``delete_all()`` method. (2020-06-06)
**************************************************

Add a new method called ``delete_all()`` that deletes all known EXIF tags in an
``Image`` object.

Add enumeration for the following tag:

* Resolution unit

This minor release addresses the following GitHub user issue:

* Removing all known EXIF values. (https://github.com/TNThieding/exif/issues/29)

This minor release contains changes submitted via GitHub pull request by the following user:

* ArgiesDario

******************************************************
[0.10.0] Add additional tag enumerations. (2020-05-31)
******************************************************

Add enumerations for the following tags:

* Exposure mode
* Exposure program
* Metering mode
* Scene capture type
* Sensing method
* White balance

**************************************************
[0.9.0] Add thumbnail image accessor. (2020-05-30)
**************************************************

Add ``get_thumbnail()`` method to extract bytes representing a thumbnail JPEG.

This patch addresses the following GitHub user issue:

* Extract thumbnail from the EXIF metadata. (https://github.com/TNThieding/exif/issues/28)

*******************************************************************************
[0.8.6] Make ``get()`` return default value if tag isn't readable. (2020-05-29)
*******************************************************************************

Previously, using ``get()`` to read a tag that can't be read by this package
raised a ``NotImplementedError``. Now, ``get()`` returns the default value (i.e.,
``None`` if not specified otherwise) if the specified tag cannot be read.

This patch addresses the following GitHub user issue:

* Method ``gets()`` raises ``NotImplementedError``. (https://github.com/TNThieding/exif/issues/30)

****************************************************
[0.8.5] Fix ``exif_version`` attribute. (2020-05-18)
****************************************************

Add support for reading ``exif_version`` attribute.

This patch addresses the following GitLab user issue:

* Reading ``exif_version`` fails with ``NotImplementedError``. (https://gitlab.com/TNThieding/exif/issues/20)

************************************************
[0.8.4] Restore Python 3.5 support. (2020-05-10)
************************************************

Remove format string usage throughout package to restore Python 3.5 support. Add Python 3.5 testing to CI/CD pipeline.

This patch addresses the following GitHub and GitLab user issues:

* Broken Python 3.5 compatibility with Release 0.8.3. (https://gitlab.com/TNThieding/exif/-/issues/21)
* Dependency on enum34 makes it impossible to build a conda package. (https://github.com/TNThieding/exif/issues/25)

This patch contains changes submitted via GitHub pull request by the following user:

* RKrahl

***************************************************
[0.8.3] Mid-April 2020 bug fix rollup. (2020-04-20)
***************************************************

This patch addresses the following GitHub user issues:

- Fix reading ASCII tags containing 3 characters or less. (See https://github.com/TNThieding/exif/issues/12
  for more information.)
- Fix `gps_longitude_ref` and `gps_latitude_ref` decoding. (See https://github.com/TNThieding/exif/issues/24
  for more information).

*****************************************************
[0.8.2] Early-March 2020 bug fix rollup. (2020-03-10)
*****************************************************

This patch addresses the following GitHub user issues:

- Update PyPI classification to more clearly indicate that this package only supports Python 3.
  (See https://github.com/TNThieding/exif/issues/20 for discussion.)
- Add read-only support for Windows XP style tags. (See https://github.com/TNThieding/exif/issues/22
  for more information.)
- Fix a benign cursor increment bug in ``_app1_metadata.py``. (See
  https://github.com/TNThieding/exif/issues/18 for more information.)

This patch also addresses the following issues:

- The ``offset_time_digitized`` was previously incorrectly mapped to ``offset_time_original``.

***************************************************
[0.8.1] Restructure tag type behavior. (2019-07-28)
***************************************************

Replace complex and duplicated ``if`` statements with polymorphic tag datatypes.

************************************************
[0.8.0] Add ``has_exif`` attribute. (2019-07-07)
************************************************

Previously, instantiating an ``Image`` with a non-EXIF file raised an ``IOError``. Now, ``Image``
instantiation always succeeds and the ``has_exif`` attribute reports whether or not the image
currently has EXIF metadata.

******************************************************
[0.7.0] Support modifying image rotation. (2019-06-23)
******************************************************

Add support for modifying metadata with the SHORT datatype (e.g., image orientation). Add
``Orientation`` enumeration to facilitate rotating images.

*******************************************
[0.6.0] Drop Python 2 support. (2019-06-16)
*******************************************

Remove legacy Python 2 syntax from code.

This release includes the following under-the-hood changes:

- Migrate repository from GitHub to GitLab (including CI/CD).
- Pylint cleanup regarding Python 3 syntax.

***************************************************
[0.5.1] Mid-April 2019 bug fix rollup. (2019-04-14)
***************************************************

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
