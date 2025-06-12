import subprocess

from adapters.gateways.get_seats.systemd_get_devices_by_seat import systemd_get_devices_by_seat
from adapters.gateways.get_seats.systemd_get_sessions_by_seat import systemd_get_sessions_by_seat
from domain.entities.device import Device
from domain.entities.seat import Seat
from adapters.gateways.get_seats.seats_reader_gateway import ISeatsReaderGateway
from typing import List

from domain.entities.session import Session


class SystemdSeatReader(ISeatsReaderGateway):
    def fetch_all_seats(self) -> List[Seat]:
        get_seats = subprocess.check_output(['loginctl', 'list-seats'], text=True)
        seats: List[Seat] = []
        print(get_seats)

        for line in get_seats.strip().split('\n')[1:]:
            if "seats listed." in line or not line:
                continue
            seat_id = line.strip()
            sessions : List[Session]  = systemd_get_sessions_by_seat(seat_id)
            devices : List[Device] = systemd_get_devices_by_seat(seat_id)
            seats.append(Seat(seat_id,devices,sessions))

        return seats
