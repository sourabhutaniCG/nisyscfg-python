"""Expert discovery and enumeration functionality for NI System Configuration."""

import typing
from typing import Any, Callable, Optional

import nisyscfg.errors
from nisyscfg import _library_singleton
from nisyscfg._lib import c_string_decode

ExpertInfo = typing.NamedTuple(
    "ExpertInfo",
    [
        ("expert_name", str),
        ("display_name", str),
        ("version", str),
    ],
)

# Provide typed wrappers for untyped callables so mypy's "no-untyped-call"
# rule is satisfied while preserving runtime behavior.
_c_string_decode: Callable[[Any], str] = c_string_decode
_get_library: Callable[[], Any] = _library_singleton.get


class ExpertInfoIterator(object):
    """Iterates over expert information returned by the system."""

    def __init__(self, handle: Optional[Any]) -> None:
        """Initialize the expert info iterator."""
        self._handle: Optional[Any] = handle
        # _library is untyped at runtime; we keep the type as Any to avoid
        # leaking implementation details while satisfying type checking.
        self._library: Any = _get_library()

    def __del__(self) -> None:
        """Release resources associated with the iterator."""
        self.close()

    def __iter__(self) -> "ExpertInfoIterator":
        """Return the iterator instance."""
        return self

    def __next__(self) -> ExpertInfo:
        """Return the next expert information entry."""
        if not self._handle:
            # TODO(tkrebes): raise RuntimeError
            raise StopIteration()
        expert_name = nisyscfg.types.simple_string()
        display_name = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        error_code = self._library.NextExpertInfo(self._handle, expert_name, display_name, version)
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return ExpertInfo(
            _c_string_decode(expert_name.value),
            _c_string_decode(display_name.value),
            _c_string_decode(version.value),
        )

    def close(self) -> None:
        """Close the expert enumeration handle."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
