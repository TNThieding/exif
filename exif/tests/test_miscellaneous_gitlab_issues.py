"""Regression tests for miscellaneous GitLab issues."""

import os

import pytest
from baseline import Baseline

from exif import Image


def test_gitlab_issue_23():
    """Regression test for GitLab issue 23.

    Verify reading ASCII tags containing a smaller length value than specified by the size field.

    """
    image_under_test = Image(os.path.join(os.path.dirname(__file__), "excess_ascii_null_bytes.jpg"))

    with pytest.warns(RuntimeWarning, match="ASCII tag contains 2 fewer bytes than specified"):
        assert image_under_test.model == Baseline("""iPhone""")

    with pytest.warns(RuntimeWarning, match="ASCII tag contains 13 fewer bytes than specified"):
        assert image_under_test.software == Baseline("""Photoshop Express""")


def test_gitlab_issue_26():
    """Regression test for GitLab issue 26.

    Verify reading lens specification where value is 0 (encoded as 0/0) does not raise ZeroDivisionError.

    """
    image_under_test = Image(os.path.join(os.path.dirname(__file__), "gitlab_issue_26.jpg"))

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
    image_under_test = Image(os.path.join(os.path.dirname(__file__), "gitlab_issue_28.jpg"))

    # Check initial value.
    assert repr(image_under_test.exposure_program) == '<ExposureProgram.APERTURE_PRIORITY: 3>'
