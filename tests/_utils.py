"""Common test utility functions."""

import sys
from typing import Any


def check_value(expected: Any, actual: Any) -> bool:
    if sys.version_info.major == 3 and sys.version_info.minor == 10:
        equal = expected in actual
    else:
        equal = expected == actual

    return equal
