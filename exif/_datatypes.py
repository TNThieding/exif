"""Package EXIF-specific datatypes."""

from plum.array import Array
from plum.int.big import UInt16, UInt32
from plum.int.little import UInt16 as UInt16_L, UInt32 as UInt32_L
from plum.int.enum import Enum
from plum.structure import DimsMember, Member, Structure, TypeMember, VariableDimsMember, VariableTypeMember


class TiffByteOrder(Enum, nbytes=2):

    """TIFF Header Byte Order Indicator"""

    LITTLE = 0x4949
    BIG = 0x4D4D


class TiffHeader(Structure):

    """TIFF Header"""

    byte_order: int = TypeMember(cls=TiffByteOrder, mapping={TiffByteOrder.LITTLE: UInt32_L, TiffByteOrder.BIG: UInt32})
    reserved: int = Member(cls=UInt16)
    ifd_offset: int = VariableTypeMember(type_member=byte_order)


class ExifType(Enum, nbytes=2, byteorder="big"):

    """EXIF Tag Types"""

    EMPTY = 0
    BYTE = 1
    ASCII = 2
    SHORT = 3
    LONG = 4
    RATIONAL = 5
    UNDEFINED = 7
    SLONG = 9
    SRATIONAL = 10


class ExifTypeLe(Enum, nbytes=2, byteorder="little"):

    """EXIF Tag Types (Little Endian)"""

    EMPTY = 0
    BYTE = 1
    ASCII = 2
    SHORT = 3
    LONG = 4
    RATIONAL = 5
    UNDEFINED = 7
    SLONG = 9
    SRATIONAL = 10


class IfdTag(Structure):

    """IFD Tag"""

    tag_id: int = Member(cls=UInt16)
    type: int = Member(cls=ExifType)
    value_count: int = Member(cls=UInt32)
    value_offset: int = Member(cls=UInt32)


class IfdTagLe(Structure):

    """IFD Tag (Little Endian)"""

    tag_id: int = Member(cls=UInt16_L)
    type: int = Member(cls=ExifTypeLe)
    value_count: int = Member(cls=UInt32_L)
    value_offset: int = Member(cls=UInt32_L)


class IfdTagArray(Array, item_cls=IfdTag):

    """IFD Tag Array"""


class IfdTagArrayLe(Array, item_cls=IfdTagLe):

    """IFD Tag Array (Little EndianO"""


class Ifd(Structure):

    """IFD SEgment"""

    count: int = DimsMember(cls=UInt16)
    tags: list = VariableDimsMember(dims_member=count, cls=IfdTagArray)
    next: int = Member(cls=UInt32)


class IfdLe(Structure):

    """IFD Segment (Little Endian)"""

    count: int = DimsMember(cls=UInt16_L)
    tags: list = VariableDimsMember(dims_member=count, cls=IfdTagArrayLe)
    next: int = Member(cls=UInt32_L)
