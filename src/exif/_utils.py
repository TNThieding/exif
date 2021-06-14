"""Utility functions."""

from exif._constants import ATTRIBUTE_ID_MAP
from exif._datatypes import ExifType


def pack_into(datatype, buffer, offset=0):
    """Pack datatype bytes into buffer."""
    buffer[offset : offset + datatype.nbytes] = datatype.ipack()


def value_fits_in_ifd_tag(tag_dt):
    """Determine if value fits inside the IFD tag itself.

    :param Structure tag_dt: IFD tag datatype instance
    :returns: value fits inside IFD tag
    :rtype: bool

    """
    is_value_in_ifd_tag_itself = (
        tag_dt.type == ExifType.ASCII and tag_dt.value_count <= 4
    )
    is_value_in_ifd_tag_itself |= tag_dt.type == ExifType.BYTE
    is_value_in_ifd_tag_itself |= tag_dt.type == ExifType.SHORT
    is_value_in_ifd_tag_itself |= tag_dt.type == ExifType.SSHORT
    is_value_in_ifd_tag_itself |= tag_dt.type == ExifType.LONG
    is_value_in_ifd_tag_itself |= tag_dt.type == ExifType.SLONG
    is_value_in_ifd_tag_itself |= tag_dt.tag_id == ATTRIBUTE_ID_MAP["exif_version"]
    is_value_in_ifd_tag_itself |= tag_dt.tag_id == ATTRIBUTE_ID_MAP["flashpix_version"]

    return is_value_in_ifd_tag_itself
