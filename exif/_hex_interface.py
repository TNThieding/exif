"""Hexadecimal string interface module."""

from exif._constants import HEX_PER_BYTE


class HexInterface(object):

    """Hexadecimal string interface class."""

    def __init__(self, hex_string):
        self._hex_string = hex_string

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
        :param int hex_string: bytes to overwrite with

        """
        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            hex_string +
            self._hex_string[offset * HEX_PER_BYTE + len(hex_string):]
        )

    def modify_number(self, offset, num_bytes, value):
        """Replace byets in the hexadecimal string with a number.

        :param int offset: starting byte to modify
        :param int num_bytes: number of bytes to store value in
        :param int value: new numeric value

        """
        self._hex_string = (
            self._hex_string[:offset * HEX_PER_BYTE] +
            hex(value).lstrip('0x').zfill(num_bytes * HEX_PER_BYTE) +
            self._hex_string[(offset + num_bytes) * HEX_PER_BYTE:]
        )

    def read(self, offset, num_bytes):
        """Read bytes in the hexadecimal string.

        :param int offset: starting byte to read
        :param int num_bytes: number of bytes to read

        """
        return self._hex_string[offset * HEX_PER_BYTE:(offset + num_bytes) * HEX_PER_BYTE]

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
