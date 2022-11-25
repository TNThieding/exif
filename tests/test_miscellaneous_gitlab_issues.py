"""Regression tests for miscellaneous GitLab issues."""

import binascii
import os
import textwrap

import pytest
from baseline import Baseline

from exif import Image, ColorSpace

from ._utils import check_value


def test_gitlab_issue_23():
    """Regression test for GitLab issue 23.

    Verify reading ASCII tags containing a smaller length value than specified by the size field.

    """
    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "excess_ascii_null_bytes.jpg")
    )

    with pytest.warns(
        RuntimeWarning, match="ASCII tag contains 2 fewer bytes than specified"
    ):
        assert image_under_test.model == Baseline("""iPhone""")

    with pytest.warns(
        RuntimeWarning, match="ASCII tag contains 13 fewer bytes than specified"
    ):
        assert image_under_test.software == Baseline("""Photoshop Express""")


def test_gitlab_issue_26():
    """Regression test for GitLab issue 26.

    Verify reading lens specification where value is 0 (encoded as 0/0) does not raise ZeroDivisionError.

    """
    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "gitlab_issue_26.jpg")
    )

    # Check initial value.
    assert image_under_test.lens_specification == (50.0, 50.0, 0, 0)

    # Change to an arbitrary minimum and maximum focal length and then back to unknown to exercise writing.
    image_under_test.lens_specification = (50.0, 50.0, 25.0, 25.0)
    image_under_test.lens_specification = (50.0, 50.0, 0, 0)
    assert image_under_test.lens_specification == (50.0, 50.0, 0, 0)


def test_gitlab_issue_28():
    """Regression test for GitLab issue 28.

    Verify support for signed short EXIF tags.

    """
    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "gitlab_issue_28.jpg")
    )

    # Check initial value.
    assert check_value(
        repr(image_under_test.exposure_program),
        "<ExposureProgram.APERTURE_PRIORITY: 3>",
    )


def test_gitlab_issue_33():
    """Regression test for GitLab issue 33.

    Smoke test to verify support for adding tags after calling ``delete_all()`` method.

    """
    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "florida_beach.jpg")
    )

    image_under_test.delete_all()
    assert not hasattr(image_under_test, "color_space")

    image_under_test.color_space = ColorSpace.UNCALIBRATED
    assert hasattr(image_under_test, "color_space")
    assert image_under_test.color_space == ColorSpace.UNCALIBRATED


def test_gitlab_issue_67():
    """Regression test for GitLab issue 67.

    Smoke test to verify the app 1 segment does not contain start markers of the next sections.
    If this is the case, adding an attribute with external data to the last IFD (GPS in this case)
    rips apart the next section, often causing a damaged file, that cannot be opened with most viewers.

    """
    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "little_endian.jpg")
    )

    # APP1 should not contain the JPEG DQT Marker
    tail = image_under_test._segments["APP1"].get_segment_bytes()[-20:]
    tailPairs = [tail[i - 2 : i] for i in range(2, len(tail) + 1)]
    assert b"\xff\xdb" not in tailPairs

    # This write would damage the quantization table
    image_under_test.gps_altitude = 1512.563022080633

    # APP1 should not contain the JPEG DQT Marker
    tail = image_under_test._segments["APP1"].get_segment_bytes()[-20:]
    tailPairs = [tail[i - 2 : i] for i in range(2, len(tail))]
    assert b"\xff\xdb" not in tailPairs

    image_under_test = Image(
        os.path.join(os.path.dirname(__file__), "gitlab_issue_67.jpg")
    )

    # APP1 should not contain the APP9 Marker
    tail = image_under_test._segments["APP1"].get_segment_bytes()[-20:]
    tailPairs = [tail[i - 2 : i] for i in range(2, len(tail) + 1)]
    assert b"\xff\xe9" not in tailPairs

    # This write would cause APP9 section to be damaged, as it contains bytes
    # that are interpreted as section starts the complete file is unreadable
    # by most viewers
    image_under_test.gps_altitude = 1512.563022080633

    # APP1 should not contain the APP9 Marker
    tail = image_under_test._segments["APP1"].get_segment_bytes()[-20:]
    tailPairs = [tail[i - 2 : i] for i in range(2, len(tail))]
    assert b"\xff\xe9" not in tailPairs
