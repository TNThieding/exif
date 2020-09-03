"""Regression tests for miscellaneous GitLab issues."""

import os

import pytest
from baseline import Baseline

from exif import Image


def test_gitlab_issue_23():
    """Regression test for Gitlab issue 23.

    Verify reading ASCII tags containing a smaller length value than specified by the size field.

    """
    image_under_test = Image(os.path.join(os.path.dirname(__file__), "excess_ascii_null_bytes.jpg"))

    with pytest.warns(RuntimeWarning, match="ASCII tag contains 2 fewer bytes than specified"):
        assert image_under_test.model == Baseline("""iPhone""")

    with pytest.warns(RuntimeWarning, match="ASCII tag contains 13 fewer bytes than specified"):
        assert image_under_test.software == Baseline("""Photoshop Express""")
