from abc import ABC, abstractmethod
from typing import List

from model.data.device import Device
from model.data.seat import Seat
from model.data.session import Session


class MultiSeatManager(ABC):
    """
    Abstract base class defining the contract for managing multi-seat systems.
    """

    @abstractmethod
    def get_seats(self) -> List[Seat]:
        """Retrieve all available seats."""
        pass

    @abstractmethod
    def get_all_sessions(self) -> List[Session]:
        """Retrieve all active sessions on the system."""
        pass

    @abstractmethod
    def get_sessions_by_seat(self, seat_id: str) -> List[Session]:
        """Get all sessions associated with a specific seat."""
        pass

    @abstractmethod
    def get_all_devices(self) -> List[Device]:
        """Retrieve all devices connected to the system."""
        pass

    @abstractmethod
    def get_devices_by_seat(self, seat_id: str) -> List[Device]:
        """Retrieve all devices attached to a specific seat."""
        pass

    @abstractmethod
    def add_device_to_seat(self, seat: Seat, device: Device) -> None:
        """Attach a device to the given seat."""
        pass

    @abstractmethod
    def remove_device_from_seat(self, seat: Seat, device_path: str) -> None:
        """Remove a device from a seat using its sysfs path."""
        pass

    @abstractmethod
    def attach_session_to_seat(self, seat: Seat, session: Session) -> None:
        """Attach a session to a seat."""
        pass

    @abstractmethod
    def detach_session_from_seat(self, seat: Seat, session_id: str) -> None:
        """Detach a session from a seat by session ID."""
        pass

    @abstractmethod
    def get_parent_device(self,  device_path: str) -> Device:
        """Return the parent Device of the given device path within the given seat."""
        pass

    @abstractmethod
    def get_children_devices(self,  device_children: List[str]) -> List[Device]:
        """Return a list of child Devices from a list of device paths."""
        pass

    @abstractmethod
    def get_device_seat(self, device_path: str) -> str:
        """
        Return the seat ID to which a device (by path) belongs.
        If no seat contains the device, return None.
        """
        pass

    @abstractmethod
    def add_seat(self, device_path: str, seat_id: str) -> None:
        """Create a new seat by attaching a device to it."""
        pass

    @abstractmethod
    def remove_seat(self, seat_id: str) -> None:
        """Remove a seat and detach all devices and sessions."""
        pass

    @abstractmethod
    def flush_all_devices(self) -> None:
        """Detach all devices from all seats."""
        pass

