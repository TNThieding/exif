"""Utility functions used when adding tags to an image's APP1 segment."""

from exif._constants import ATTRIBUTE_ID_MAP


def value_fits_in_ifd_tag(tag_dt, exif_type_cls):
    """Determine if value fits inside the IFD tag itself.

    :param Structure tag_dt: IFD tag datatype instance
    :param Enum exif_type_cls: EXIF type enumeration
    :returns: value fits inside IFD tag
    :rtype: bool

    """
    is_value_in_ifd_tag_itself = tag_dt.type == exif_type_cls.ASCII and tag_dt.value_count <= 4
    is_value_in_ifd_tag_itself |= tag_dt.type == exif_type_cls.BYTE
    is_value_in_ifd_tag_itself |= tag_dt.type == exif_type_cls.SHORT
    is_value_in_ifd_tag_itself |= tag_dt.type == exif_type_cls.SSHORT
    is_value_in_ifd_tag_itself |= tag_dt.type == exif_type_cls.LONG
    is_value_in_ifd_tag_itself |= tag_dt.type == exif_type_cls.SLONG
    is_value_in_ifd_tag_itself |= tag_dt.tag_id == ATTRIBUTE_ID_MAP["exif_version"]
    is_value_in_ifd_tag_itself |= tag_dt.tag_id == ATTRIBUTE_ID_MAP["flashpix_version"]

    return is_value_in_ifd_tag_itself
