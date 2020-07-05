"""Test modifying EXIF attributes and getting new file contents."""

import binascii
import os
import textwrap

from exif import Image
from exif.tests.get_file_baselines import GRAND_CANYON_THUMBNAIL, MODIFIED_NOISE_FILE_HEX_BASELINE


def test_get_file():
    """Verify that an image is writable to a file after modifying its EXIF metadata.

    Assert the produced file is equivalent to a known baseline.

    """
    image = Image(os.path.join(os.path.dirname(__file__), 'noise.jpg'))
    image.software = "Python"

    file_hex = binascii.hexlify(image.get_file()).decode("utf-8")
    assert '\n'.join(textwrap.wrap(file_hex, 90)) == MODIFIED_NOISE_FILE_HEX_BASELINE


def test_get_thumbnail():
    """Test file contents of thumbnail image."""
    with open(os.path.join(os.path.dirname(__file__), 'grand_canyon.jpg'), 'rb') as image_file:
        image = Image(image_file)

    file_hex = binascii.hexlify(image.get_thumbnail()).decode("utf8")
    assert '\n'.join(textwrap.wrap(file_hex, 90)) == GRAND_CANYON_THUMBNAIL
