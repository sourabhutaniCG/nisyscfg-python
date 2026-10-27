from __future__ import absolute_import

import locale
import sys

import six

if sys.platform.startswith("win"):
    # On Windows, nisyscfg uses the system code page for the decoding of C-strings
    def get_syscfg_locale():
        """Return the locale used by NI System Configuration."""
        return locale.getlocale()[1] or locale.getdefaultlocale()[1] or "ascii"

else:
    # On other OSes, nisyscfg uses ISO-8859-1 (Latin1) for the decoding of C-strings
    def get_syscfg_locale():
        """Return the locale used by NI System Configuration."""
        return "ISO-8859-1"


def c_string_encode(value):
    """Encode a Python string for use with the C API."""
    if isinstance(value, six.text_type):
        return value.encode(get_syscfg_locale())
    return value


def c_string_decode(value):
    """Decode a string returned by the C API."""
    if isinstance(value, six.binary_type):
        return value.decode(get_syscfg_locale())
    return value
