"""Tests for native operations that may return a NULL details pointer."""

from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

import nisyscfg.errors
import nisyscfg.hardware_resource
import nisyscfg.system
import nisyscfg.types


@pytest.fixture
def hardware_resource_and_library() -> (
    Iterator[tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock]]
):
    library = MagicMock()
    library.CloseHandle.return_value = nisyscfg.errors.Status.OK
    with patch("nisyscfg.hardware_resource._library_singleton.get", return_value=library):
        resource = nisyscfg.hardware_resource.HardwareResource(nisyscfg.types.ResourceHandle(1))
        yield resource, library
        resource.close()


@pytest.fixture
def session_and_library() -> Iterator[tuple[nisyscfg.system.Session, MagicMock]]:
    library = MagicMock()
    library.InitializeSession.return_value = nisyscfg.errors.Status.OK
    library.CloseHandle.return_value = nisyscfg.errors.Status.OK
    with patch("nisyscfg._library_singleton.get", return_value=library):
        session = nisyscfg.system.Session()
        yield session, library
        session.close()


def test_hardware_resource_save_changes_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.SaveResourceChanges.return_value = nisyscfg.errors.Status.OK

    result = resource.save_changes()

    assert result.details == ""
    library.FreeDetailedString.assert_not_called()


def test_hardware_resource_self_calibrate_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.SelfCalibrateHardware.return_value = nisyscfg.errors.Status.OK

    assert resource.self_calibrate() == ""
    library.FreeDetailedString.assert_not_called()


def test_hardware_resource_self_test_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.SelfTestHardware.return_value = nisyscfg.errors.Status.OK

    assert resource.self_test() == ""
    library.FreeDetailedString.assert_not_called()


def test_hardware_resource_upgrade_firmware_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.UpgradeFirmwareVersion.return_value = nisyscfg.errors.Status.OK

    result = resource.upgrade_firmware(version="1.0")

    assert result.details == ""
    library.FreeDetailedString.assert_not_called()


def test_hardware_resource_firmware_status_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.CheckFirmwareStatus.return_value = nisyscfg.errors.Status.OK

    result = resource.firmware_status

    assert result.details == ""
    library.FreeDetailedString.assert_not_called()


def test_hardware_resource_delete_with_null_details(
    hardware_resource_and_library: tuple[nisyscfg.hardware_resource.HardwareResource, MagicMock],
) -> None:
    resource, library = hardware_resource_and_library
    library.DeleteResource.return_value = nisyscfg.errors.Status.OK

    result = resource.delete()

    assert result.details == ""
    library.FreeDetailedString.assert_not_called()


def test_session_save_changes_with_null_details(
    session_and_library: tuple[nisyscfg.system.Session, MagicMock],
) -> None:
    session, library = session_and_library
    library.SaveSystemChanges.return_value = nisyscfg.errors.Status.OK

    result = session.save_changes()

    assert result.details == ""
    library.FreeDetailedString.assert_not_called()


def test_session_get_status_description_with_null_details(
    session_and_library: tuple[nisyscfg.system.Session, MagicMock],
) -> None:
    session, library = session_and_library
    library.GetStatusDescription.return_value = nisyscfg.errors.Status.OK

    result = session._get_status_description(nisyscfg.errors.Status.OK)

    assert result == ""
    library.FreeDetailedString.assert_not_called()
