"""Tests for software dependency information."""

from typing import Any
from unittest.mock import MagicMock, patch

import nisyscfg.dependency_info
import nisyscfg.errors
import nisyscfg.types


def test_dependency_info_iterator_decodes_component_strings() -> None:
    """Verify that dependency component fields are returned as strings."""
    library = MagicMock()

    def next_dependency_info(*args: Any) -> nisyscfg.errors.Status:
        args[1].value = b"depender.id"
        args[2].value = b"1.2.3"
        args[3].value = b"Depender"

        args[5].value = b"dependee.id"
        args[6].value = b"4.5.6"
        args[7].value = b"Dependee"

        return nisyscfg.errors.Status.OK

    library.NextDependencyInfo.side_effect = next_dependency_info
    library.CloseHandle.return_value = nisyscfg.errors.Status.OK

    with patch(
        "nisyscfg.dependency_info._library_singleton.get",
        return_value=library,
    ):
        iterator = nisyscfg.dependency_info.DependencyInfoIterator(
            nisyscfg.types.EnumDependencyHandle(1)
        )
        try:
            dependency = next(iterator)
        finally:
            iterator.close()

    assert dependency.depender.id == "depender.id"
    assert dependency.depender.version == "1.2.3"
    assert dependency.depender.title == "Depender"

    assert dependency.dependee.id == "dependee.id"
    assert dependency.dependee.version == "4.5.6"
    assert dependency.dependee.title == "Dependee"

    assert isinstance(dependency.depender.id, str)
    assert isinstance(dependency.depender.version, str)
    assert isinstance(dependency.depender.title, str)

    assert isinstance(dependency.dependee.id, str)
    assert isinstance(dependency.dependee.version, str)
    assert isinstance(dependency.dependee.title, str)

    library.NextDependencyInfo.assert_called_once()
    library.CloseHandle.assert_called_once()
