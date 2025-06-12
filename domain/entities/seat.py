from typing import List

from domain.entities.device import Device
from domain.entities.session import Session


class Seat:

    def __init__(self, seat_id: str, devices:List[Device]=None, sessions:List[Session]=None):
        if sessions is None:
            sessions = []
        if devices is None:
            devices = []
        self.seat_id = seat_id
        self.devices: List[Device] =  devices
        self.sessions: List[Session] = sessions

    def add_device(self, device: Device):
        if device.path not in [d.path for d in self.devices]:
            self.devices.append(device)

    def remove_device(self, path: str):
        self.devices = [d for d in self.devices if d.path != path]

    def attach_session(self, session_id: Session):
        if session_id not in self.sessions:
            self.sessions.append(session_id)

    def detach_session(self, session_id: str):
        self.sessions = [s for s in self.sessions if s.session_id != session_id]

    def list_devices(self):
        return self.devices

    def list_sessions(self):
        return self.sessions

    def has_device(self, device_path: str) -> bool:
        return any(d.path == device_path for d in self.devices)

    def __repr__(self):
        return f"<Seat {self.seat_id} | Devices: {len(self.devices)} | Sessions: {self.sessions}>"