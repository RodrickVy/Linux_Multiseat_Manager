import os
from typing import List
import subprocess

from controllers.device_extractor import DevicesExtractor
from model.data.device import Device
from model.data.seat import Seat
from model.data.session import Session
from model.multiseat_manager import MultiSeatManager


class SystemdMultiSeatManager(MultiSeatManager):



    def get_seats(self) -> List[Seat]:
        get_seats = subprocess.check_output(['loginctl', 'list-seats'], text=True)
        seats: List[Seat] = []


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
        # Run the whole pipeline as a shell command
        cmd = f"loginctl seat-status {seat_id} | grep /sys/devices"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        extractor = DevicesExtractor(output)

        return  extractor.extract_devices()


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

    def get_parent_device(self,  device_path: str) -> Device:
        devices = self.get_all_devices()
        target_device = next((d for d in devices if d.path == device_path), None)

        if not target_device or not target_device.parent_path:
            return None

        return next((d for d in devices if d.path == target_device.parent_path), None)

    def get_children_devices(self, device_children: List[str]) -> List[Device]:
        devices = self.get_all_devices()
        children = [device for device in devices if device.path in device_children]
        return children

    def get_device_seat(self, device_path: str) -> str:
        """
        Searches all seats to find the one that contains the given device.
        """
        seats = self.get_seats()
        for seat in seats:
            for device in seat.devices:
                if device.path == device_path:
                    return seat.seat_id
        return None

    def add_seat(self, device_path: str, seat_id: str) -> None:
        """
        Creates a new seat by attaching the given device to the given seat_id.
        """
        try:
            subprocess.check_call(["loginctl", "attach", seat_id, device_path])
        except subprocess.CalledProcessError as e:
            print(f"[Error] Could not attach {device_path} to {seat_id}: {e}")

    def remove_seat(self, seat_id: str) -> None:
        """
        Detach all devices from the seat to effectively 'remove' it.
        Systemd does not support explicitly deleting a seat; removing all its devices achieves this.
        """
        devices = self.get_devices_by_seat(seat_id)
        for device in devices:
            try:
                subprocess.check_call(["loginctl", "detach", device.path])
            except subprocess.CalledProcessError as e:
                print(f"[Error] Failed to detach {device.path} from seat {seat_id}: {e}")

    def flush_all_devices(self) -> None:
        """
        Uses loginctl to flush all devices system-wide.
        """
        try:
            subprocess.check_call(["loginctl", "flush-devices"])
        except subprocess.CalledProcessError as e:
            print(f"[Error] Could not flush all devices: {e}")


