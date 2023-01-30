#############
Release Notes
#############

*******************************************************
[1.6.0] Support ``rating`` and ``rating_percent`` tags.
*******************************************************

Now, users can access the ``rating`` and ``rating_percent`` EXIF tags.

This release contains changes submitted via GitLab merge request by the following user:

* Gerald Triendl (TriG81)


**************************************************************
[1.5.0] Support ``photographic_sensitivity`` tag. (2023-01-09)
**************************************************************

Now, users can read and write the ``photographic_sensitivity`` EXIF tag.

This release contains changes submitted via GitHub merge request by the following user:

* Luca Di Leo (HeDo88TH)


***********************************************************
[1.4.2] Improve data packing when adding tags. (2022-12-28)
***********************************************************

Previously, new tags added to an image were always placed at the end of the metadata section. Now, new tags are inserted
directly after the last tag value block and not just at the end of the metadata section. Therefore, the data is inserted
before the trailing unused bytes.

This patch contains changes submitted via GitLab merge request by the following user:

* Patrick (buergi)


**************************************************************************
[1.4.1] Fix logic for checking if a value fits in an IFD tag. (2022-12-23)
**************************************************************************

Previously, modifying EXIF attribute values unintentionally changed untouched attributes
(e.g., ``components_configuration`` and ``subject_area``) due to a bug within the helper
function ``value_fits_in_ifd_tag``.

This patch addresses the following GitLab user issue:

* Modifying EXIF changes untouched attributes. (https://gitlab.com/TNThieding/exif/-/issues/68)

This patch contains changes submitted via GitLab merge request by the following user:

* Patrick (buergi)


*************************************************************
[1.4.0] Late-November 2022 merge request rollup. (2022-11-25)
*************************************************************

This release includes community-contributed merge requests:

* Add ``focal_plane_x_resolution`` and ``focal_plane_y_resolution`` to the attribute mapping. (https://gitlab.com/TNThieding/exif/merge_requests/55)
* Fix incorrect determination of APP1 size. (https://gitlab.com/TNThieding/exif/-/merge_requests/56)
* Fix wrong offset of newly-created ITD. (https://gitlab.com/TNThieding/exif/-/merge_requests/59)
* Add support for multi-valued signed rationals. (https://gitlab.com/TNThieding/exif/-/merge_requests/60)

Thank you to the following users for their contributions:

* Patrick (buergi)
* simonschindler


*******************************************************************
[1.3.5] Support initial stable release of ``plum-py``. (2022-04-17)
*******************************************************************

Update package to support the initial stable release of its ``plum-py`` dependency.


************************************************************
[1.3.4] Decode Windows XP style tags as UTF-16. (2021-12-09)
************************************************************

Previously, the package decoded ASCII characters within Windows XP style tags. Now, the
package decodes Windows XP style tags as UTF-16.

This patch addresses the following GitLab user issue:

* ``xp_comment`` and other Windows XP tags don't handle Unicode strings correctly.
  (https://gitlab.com/TNThieding/exif/-/issues/53)


*******************************************************************
[1.3.3] Omit unknown values from ``get_all()`` method. (2021-11-07)
*******************************************************************

Previously, ``get_all()`` did not catch exceptions when reading each EXIF tag. If a single
attribute had an incorrectly-encoded value, the ``get_all()`` method raised an exception.
Now, the ``get_all()`` method catches exceptions due to unknown or unreadable values and
logs them as a warning.

This patch addresses the following GitLab user issue:

* ``ValueError: 0 is not a valid Orientation`` returned from the ``Image.get_all()``.
  method (https://gitlab.com/TNThieding/exif/-/issues/52)


**********************************************************
[1.3.2] Add support for writing various tags. (2021-09-04)
**********************************************************

Previously, attempting to add the following tags to an image raised an ``AttributeError``:

* Body Serial Number
* ISO Speed
* Lens Specification
* Lens Make
* Lens Model
* Lens Serial Number

This patch addresses the following GitLab user issue:

* Trouble setting tags. (https://gitlab.com/TNThieding/exif/-/issues/48)


*******************************************************************
[1.3.1] Fix value of ``SceneCaptureType.NIGHT_SCENE``. (2021-07-03)
*******************************************************************

Previously, ``SceneCaptureType.NIGHT_SCENE`` erroneously had a value of ``2``. Now, it has a value of ``3`` in
accordance with the EXIF specification.

This patch contains changes submitted via GitLab merge request by the following user:

* Alex Mykyta (amykyta3)


***********************************************************
[1.3.0] Consume latest version of ``plum-py``. (2021-06-13)
***********************************************************

Overhaul package internals to leverage ``plum-py`` version ``0.5.0`` and higher. Since the ``plum-py`` package only
supports Python 3.7 and higher, this release drops support for Python 3.6.


****************************************************
[1.2.2] Late-April 2021 bug fix rollup. (2021-04-23)
****************************************************

This patch addresses the following GitLab user issues:

* Add a workaround for ``flash`` attribute in Python 3.10 to temporarily address bit field ``TypeError``.
  (Upstream ``plum-py`` Issue: https://gitlab.com/dangass/plum/-/issues/129)
* ``UnpackError`` occurs when reading a bad IFD. (https://gitlab.com/TNThieding/exif/-/issues/38)


******************************************************************************
[1.2.1] Preserve empty IFDs and EXIF version in ``delete_all()``. (2021-03-23)
******************************************************************************

Previously, attempting to re-add EXIF tags to an image after calling ``delete_all()`` on it raised a ``RuntimeError``
since it removed the EXIF version tag and the IFD structure. Now, ``delete_all()`` still removes user-facing tags but
preserves the EXIF version number and the empty IFD structures and their pointers. This enables users to add tags back
to an image after using ``delete_all()``.

This patch addresses the following GitLab user issue:

* ``RuntimeError`` when adding tags after calling ``delete_all()``. (https://gitlab.com/TNThieding/exif/-/issues/33)


******************************************************************
[1.2.0] Add ``get_all()`` and ``list_all()`` methods. (2021-02-06)
******************************************************************

Add ``list_all()`` method that returns a list of all EXIF tags in an image (without including method names and unknown
tags like ``dir()`` includes). Similarly, add ``get_all()`` method that generates a dictionary mapping each tag names to
its value.

This patch addresses the following GitLab user issue:

* API for retrieving all EXIF tags. (https://gitlab.com/TNThieding/exif/-/issues/32)


**************************************************
[1.1.0] Add type hints to public API. (2021-02-04)
**************************************************

Update ``Image`` class to include ``mypy``-compliant type hints.


******************************************************************************************
[1.0.5] Fix corruption errors when adding tags to previously non-EXIF images. (2021-01-23)
******************************************************************************************

Previously, adding EXIF tags to non-EXIF images resulted in an incorrectly-calculated APP1 segment length value. This
resulted in some image tools and libraries reporting that the file was corrupt. Now, the APP1 segment length value is
calculated correctly by excluding the APP1 marker length from the segment length.

This patch addresses the following GitLab user issue:

* Corrupt JPEG data error caused by writing EXIF data. (https://gitlab.com/TNThieding/exif/-/issues/30)


*****************************************************************************
[1.0.4] Fix adding focal length and user comment tags to images. (2020-11-28)
*****************************************************************************

Previously, attempting to add either a focal length or user comment  tag to an image resulted in an ``AttributeError``.
In addition, this patch changes attribute getters and setters such that they are not case-sensitive (e.g.,
``image.Copyright`` is treated the same as ``image.copyright``).

This patch addresses the following GitLab user issue:

* Cannot add user comments to images without preexisting metadata. (https://gitlab.com/TNThieding/exif/issues/24)

This release includes the following under-the-hood changes:

* Don't distribute unit tests with the packaged source code (e.g., when installing via ``pip``).


****************************************************************
[1.0.3] Fix ``ValueError`` when SSHORT are present. (2020-11-15)
****************************************************************

Previously, reading signed short integers resulted in a ``ValueError``.

This patch addresses the following GitLab user issue:

* Signed short integers in EXIF are not supported. (https://gitlab.com/TNThieding/exif/issues/28)

This patch contains changes submitted via GitLab merge request by the following user:

* Justin Saunders (jumaka1)


*****************************************************************************************************
[1.0.2] Fix ``ZeroDivisionError`` when reading lens specification with unknown F number. (2020-10-18)
*****************************************************************************************************

Previously, reading the lens specification attribute where the F values were
unknown resulted in a ``ZeroDivisionError`` since unknown is encoded as 0/0.
Now, the value is returned as ``0`` and the exception is no longer raised.

This patch addresses the following GitLab user issue:

* ``ZeroDivisionError`` reported when reading ``lens_specification``. (https://gitlab.com/TNThieding/exif/issues/26)


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
