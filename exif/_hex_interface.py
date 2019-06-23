"""Hexadecimal string interface module."""

from exif._constants import EXIF_BIG_ENDIAN_HEADER, EXIF_LITTLE_ENDIAN_HEADER, HEX_PER_BYTE


class HexInterface:

    """Hexadecimal string interface class."""

    def __init__(self, hex_string):
        self.endianness = EXIF_BIG_ENDIAN_HEADER
        self._hex_string = hex_string

    @staticmethod
    def _change_endian(hexadecimal_string):
        return "".join(reversed(
            [hexadecimal_string[i:i+2] for i in range(0, len(hexadecimal_string), 2)]))

    def delete(self, offset, num_bytes):
        """Delete a sequence of hexadecimal digits from the hexadecimal string.

        :param int offset: starting byte to delete
        :param int num_bytes: number of bytes to delete

        """
        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            self._hex_string[(offset + num_bytes) * HEX_PER_BYTE:]
        )

    def get_hex_string(self):
        """Get the equivalent hexadecimal string.

        :returns: hexadecimal string
        :rtype: str

        """
        return self._hex_string

    def insert_null(self, offset, num_bytes):
        """Insert empty bytes (i.e. '00') into the hexadecimal string.

        :param int offset: byte to insert at
        :param int num_bytes: number of empty bytes to insert

        """
        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            '0' * num_bytes * HEX_PER_BYTE +
            self._hex_string[offset * HEX_PER_BYTE:]
        )

    def modify_hex(self, offset, hex_string):
        """Replace bytes in the hexadecimal string with a new string.

        :param int offset: starting byte to modify
        :param str hex_string: bytes to overwrite with

        """
        if isinstance(hex_string, bytes):
            hex_string = hex_string.decode("utf8")

        if self.endianness == EXIF_LITTLE_ENDIAN_HEADER:
            hex_string = self._change_endian(hex_string)

        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            hex_string +
            self._hex_string[offset * HEX_PER_BYTE + len(hex_string):]
        )

    def modify_number(self, offset, num_bytes, value):
        """Replace bytes in the hexadecimal string with a number.

        :param int offset: starting byte to modify
        :param int num_bytes: number of bytes to store value in
        :param int value: new numeric value

        """
        number_hex_bytes = hex(value).lstrip('0x').zfill(num_bytes * HEX_PER_BYTE)

        if self.endianness == EXIF_LITTLE_ENDIAN_HEADER:
            number_hex_bytes = self._change_endian(number_hex_bytes)

        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            number_hex_bytes +
            self._hex_string[(offset + num_bytes) * HEX_PER_BYTE:]
        )

    def read(self, offset, num_bytes):
        """Read bytes in the hexadecimal string.

        :param int offset: starting byte to read
        :param int num_bytes: number of bytes to read

        """
        hex_bytes = self._hex_string[offset * HEX_PER_BYTE:(offset + num_bytes) * HEX_PER_BYTE]

        if self.endianness == EXIF_LITTLE_ENDIAN_HEADER:
            hex_bytes = self._change_endian(hex_bytes)

        if len(hex_bytes) != num_bytes * HEX_PER_BYTE:
            raise ValueError("byte offset exceeds length of segment")

        return hex_bytes

    def set_endianness(self, endian_constant):
        """Set the endianness of the byte string.

        :param endian_constant: endian marker constant
        :type endian_constant: str (EXIF_BIG_ENDIAN_HEADER or EXIF_LITTLE_ENDIAN_HEADER)

        """
        assert endian_constant in [EXIF_BIG_ENDIAN_HEADER, EXIF_LITTLE_ENDIAN_HEADER]
        self.endianness = endian_constant

    def wipe(self, offset, num_bytes):
        """Wipe clear bytes in the hexadecimal string.

        :param int offset: starting byte to wipe
        :param int num_bytes: bytes to wipe (i.e. set to zero)

        """
        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            '0' * num_bytes * HEX_PER_BYTE +
            self._hex_string[(offset + num_bytes) * HEX_PER_BYTE:]
        )
