import os
from typing import List
import subprocess

from model.data.device import Device
from model.data.seat import Seat
from model.data.session import Session
from model.multiseat_manager import MultiSeatManager


class SystemdMultiSeatManager(MultiSeatManager):



    def get_seats(self) -> List[Seat]:
        get_seats = subprocess.check_output(['loginctl', 'list-seats'], text=True)
        seats: List[Seat] = []
        print(get_seats)

        for line in get_seats.strip().split('\n')[1:]:
            if "seats listed." in line or not line:
                continue
            seat_id = line.strip()
            sessions: List[Session] = self.get_sessions_by_seat(seat_id)
            devices: List[Device] = self.get_devices_by_seat(seat_id)
            seats.append(Seat(seat_id, devices, sessions))

        return seats


    def get_all_sessions(self) -> List[Session]:
        output = subprocess.check_output(['loginctl', 'list-sessions'], text=True)
        sessions = []

        for line in output.strip().split('\n')[1:]:  # Skip header line
            parts = line.split()
            if len(parts) < 8:
                continue

            session_id, uid, user, seat, tty, class_type, state, remote = parts[:8]


            session = Session(
                session_id=session_id,
                user=user,
                seat=seat,
                tty=tty,
                class_type=class_type,
                state=state,
                remote=(remote.lower() == "yes"),
                active=(state.lower() == "active")
            )
            sessions.append(session)

        return sessions


    def get_sessions_by_seat(self, seat_id: str) -> List[Session]:
        return list(filter(lambda s: s.seat == seat_id,self.get_all_sessions()))

    def get_all_devices(self) -> List[Device]:
        devices = []
        for seat in self.get_seats():
            devices.extend(seat.devices)
        return devices

    def get_devices_by_seat(self, seat_id: str) -> List[Device]:
        try:
            # Run the whole pipeline as a shell command
            cmd = f"loginctl seat-status {seat_id} | grep /sys/devices"
            output = subprocess.check_output(cmd, shell=True, text=True).strip()

            devices = []

            for line in output.splitlines():
                parts = line.strip().split()
                if not parts:
                    continue

                # First part is always the sysfs path
                path = parts[0]

                # Second part (like input:input4) gives us the type
                type_info = parts[1] if len(parts) > 1 else "unknown"
                type_ = type_info.split(":")[0]

                # Use the basename of the path as a fallback name
                name = os.path.basename(path)

                devices.append(Device(path=path, type_=type_, name=name))

            return devices

        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to get devices for seat '{seat_id}': {e}")
            return []

    def add_device_to_seat(self, seat: Seat, device: Device) -> None:
        """
        Attach a device to the given seat using its sysfs path.
        Equivalent to: loginctl attach seatX /sys/devices/...
        """
        try:
            subprocess.check_call([
                "loginctl", "attach", seat.seat_id, device.path
            ])
            print(f"[Info] Attached device {device.path} to seat {seat.seat_id}")
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to attach device: {e}")

    def remove_device_from_seat(self, seat: Seat, device_path: str) -> None:
        """
        Detach a device from a seat using its sysfs path.
        Equivalent to: loginctl detach /sys/devices/...
        """
        try:
            subprocess.check_call([
                "loginctl", "detach", device_path
            ])
            print(f"[Info] Detached device {device_path} from seat {seat.seat_id}")
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to detach device: {e}")

    def attach_session_to_seat(self, seat: Seat, session: Session) -> None:
        """
        Attach a session to the given seat.
        Equivalent to: loginctl attach seatX <session_id>
        """
        try:
            subprocess.check_call([
                "loginctl", "attach", seat.seat_id, session.session_id
            ])
            print(f"[Info] Attached session {session.session_id} to seat {seat.seat_id}")
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to attach session: {e}")

    def detach_session_from_seat(self, seat: Seat, session_id: str) -> None:
        """
        Detach (terminate) a session from a seat.
        Equivalent to: loginctl terminate-session <session_id>
        """
        try:
            subprocess.check_call([
                "loginctl", "terminate-session", session_id
            ])
            print(f"[Info] Terminated session {session_id} from seat {seat.seat_id}")
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to terminate session: {e}")

