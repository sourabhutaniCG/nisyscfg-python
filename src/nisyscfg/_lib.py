from __future__ import absolute_import

import locale
import sys
from typing import Union, Optional, Any

import six  # type: ignore[import-untyped]


if sys.platform.startswith("win"):
    # On Windows, nisyscfg uses the system code page for the decoding of C-strings
    def get_syscfg_locale() -> str:
        """Return the locale used by NI System Configuration."""
        return locale.getlocale()[1] or locale.getdefaultlocale()[1] or "ascii"

else:
    # On other OSes, nisyscfg uses ISO-8859-1 (Latin1) for the decoding of C-strings
    def get_syscfg_locale() -> str:
        """Return the locale used by NI System Configuration."""
        return "ISO-8859-1"


def c_string_encode(value: Optional[Union[str, bytes]]) -> Optional[bytes]:
    """Encode a Python string for use with the C API.

    Accept None and return None so callers can pass it directly to C APIs
    that expect a NULL pointer.
    """
    if value is None:
        return None
    # Use built-in str/bytes checks so type checkers can narrow the type.
    if isinstance(value, str):
        return value.encode(get_syscfg_locale())
    # value is bytes at runtime here
    return value


def c_string_decode(value: Optional[Union[bytes, str]]) -> str:
    """Decode a string returned by the C API.

    Treat None as an empty string for callers that expect a Python str.
    """
    if value is None:
        return ""
    # Use built-in bytes/str checks so type checkers can narrow the type.
    if isinstance(value, bytes):
        return value.decode(get_syscfg_locale())
    # value is str at runtime here
    return value
