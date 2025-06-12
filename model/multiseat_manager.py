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
