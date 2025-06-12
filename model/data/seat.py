from typing import List

from model.data.device import Device
from model.data.session import Session


class Seat:

    def __init__(self, seat_id: str, devices:List[Device]=None, sessions:List[Session]=None):
        if sessions is None:
            sessions = []
        if devices is None:
            devices = []
        self.seat_id = seat_id
        self.devices: List[Device] =  devices
        self.sessions: List[Session] = sessions