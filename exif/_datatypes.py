"""Package EXIF-specific datatypes."""

from enum import IntFlag

from plum.array import Array
from plum.int.big import UInt16, UInt32
from plum.int.bitfields import BitFields, BitField
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
    SSHORT = 8
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
    SSHORT = 8
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

    """IFD Tag Array (Little Endian)"""


class Ifd(Structure):

    """IFD Segment"""

    count: int = DimsMember(cls=UInt16)
    tags: list = VariableDimsMember(dims_member=count, cls=IfdTagArray)
    next: int = Member(cls=UInt32)


class IfdLe(Structure):

    """IFD Segment (Little Endian)"""

    count: int = DimsMember(cls=UInt16_L)
    tags: list = VariableDimsMember(dims_member=count, cls=IfdTagArrayLe)
    next: int = Member(cls=UInt32_L)


class FlashReturn(IntFlag):

    """Flash status of returned light."""

    NO_STROBE_RETURN_DETECTION_FUNCTION = 0
    RESERVED = 1
    STROBE_RETURN_LIGHT_DETECTED = 2
    STROBE_RETURN_LIGHT_NOT_DETECTED = 3


class FlashMode(IntFlag):

    """Flash mode of the camera."""

    UNKNOWN = 0
    COMPULSORY_FLASH_FIRING = 1
    COMPULSORY_FLASH_SUPPRESSION = 2
    AUTO_MODE = 3


class Flash(BitFields, nbytes=1):

    """Status of the camera's flash when the image was taken. (Reported by the ``flash`` tag.)"""

    flash_fired: bool = BitField(size=1)
    flash_return: FlashReturn = BitField(size=2)
    flash_mode: FlashMode = BitField(size=2)
    flash_function_not_present: bool = BitField(size=1)
    red_eye_reduction_supported: bool = BitField(size=1)
    reserved: int = BitField(size=1)
