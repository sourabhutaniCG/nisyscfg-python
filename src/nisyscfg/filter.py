"""Hardware filter functionality for NI System Configuration."""

import ctypes

from typing import Any, Optional, TYPE_CHECKING

import nisyscfg.errors
import nisyscfg.properties
import nisyscfg.xnet.properties
from nisyscfg._lib import c_string_encode


@nisyscfg.properties.PropertyBag(nisyscfg.properties.Filter)  # type: ignore[arg-type]
@nisyscfg.properties.PropertyBag(nisyscfg.xnet.properties.Filter, expert="xnet")  # type: ignore[arg-type]
class Filter(object):
    _handle: Optional["nisyscfg.types.FilterHandle"]

    """Represents a hardware resource filter."""

    def __init__(self, session: "nisyscfg.types.SessionHandle") -> None:
        """Initialize a hardware filter."""
        self._handle = nisyscfg.types.FilterHandle()
        # The library singleton is dynamically typed; treat it as Any locally.
        from typing import Any, cast

        self._library: Any = nisyscfg._library_singleton.get()  # type: ignore[no-untyped-call]
        # PropertyAccessor has untyped parameters; ignore the untyped-call error here.
        self._property_accessor: "nisyscfg.properties.PropertyAccessor" = (
            nisyscfg.properties.PropertyAccessor(setter=self._set_property_with_type)  # type: ignore[no-untyped-call]
        )
        # ctypes.pointer expects a C compatible handle; mypy can't verify the dynamic ctypes types here.
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))  # type: ignore[arg-type]
        nisyscfg.errors.handle_error(self, error_code)

    def __del__(self) -> None:
        """Release the filter handle."""
        self.close()

    def close(self) -> None:
        """Close the filter handle."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _set_property_with_type(self, id: int, value: Any, c_type: type, nisyscfg_type: int) -> None:
        if c_type == ctypes.c_char_p:
            # c_string_encode is untyped; ignore here.
            value = c_string_encode(value)  # type: ignore[no-untyped-call]
        elif issubclass(c_type, nisyscfg.enums.BaseEnum) or issubclass(
            c_type, nisyscfg.enums.BaseFlag
        ):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        # The SetFilterPropertyWithType call is to a C library; mypy cannot type-check it.
        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)  # type: ignore[no-untyped-call]
        nisyscfg.errors.handle_error(self, error_code)
