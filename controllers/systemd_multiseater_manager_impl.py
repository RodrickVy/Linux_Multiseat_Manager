import subprocess
from typing import List, Optional

from controllers.device_extractor import DevicesExtractor
from model.app_feedback import AppFeedback
from model.data.device import Device
from model.data.seat import Seat
from model.data.session import Session
from model.multiseat_manager import MultiSeatManager


class SystemdMultiSeatManager(MultiSeatManager):
    def __init__(self, feedback_listener=None, prompt_inputs_request_listener=None):
        super().__init__(feedback_listener, prompt_inputs_request_listener)

    def shellRun(self, command: List[str], function_name: str) -> Optional[str]:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            stderr_message = result.stderr.strip() or "Unknown error"
            if hasattr(self, 'feedback_listener') and callable(self.feedback_listener):
                feedback = AppFeedback.error(
                    message=f"Failed to run command: {' '.join(command)}\n{stderr_message}",
                    code=result.returncode,
                    function=function_name
                )
                self.feedback_listener(feedback)
        return result.stdout.strip()

    def get_seats(self) -> List[Seat]:
        output = self.shellRun(['loginctl', 'list-seats'], "get_seats")
        if output is None:
            return []

        seats = []
        for line in output.strip().split('\n')[1:]:
            if "seats listed." in line or not line:
                continue
            seat_id = line.strip()
            sessions = self.get_sessions_by_seat(seat_id)
            devices = self.get_devices_by_seat(seat_id)
            seats.append(Seat(seat_id, devices, sessions))
        return seats

    def get_all_sessions(self) -> List[Session]:
        output = self.shellRun(['loginctl', 'list-sessions'], "get_all_sessions")
        if output is None:
            return []

        sessions = []
        for line in output.strip().split('\n')[1:]:
            parts = line.split()
            if len(parts) < 8:
                continue
            session_id, uid, user, seat, tty, class_type, state, remote = parts[:8]
            sessions.append(Session(
                session_id=session_id, user=user, seat=seat, tty=tty,
                class_type=class_type, state=state,
                remote=(remote.lower() == "yes"), active=(state.lower() == "active")
            ))
        return sessions

    def get_sessions_by_seat(self, seat_id: str) -> List[Session]:
        return [s for s in self.get_all_sessions() if s.seat == seat_id]

    def get_all_devices(self) -> List[Device]:
        devices = []
        for seat in self.get_seats():
            devices.extend(seat.devices)
        return devices

    def get_devices_by_seat(self, seat_id: str) -> List[Device]:
        output = self.shellRun(["bash", "-c", f"loginctl seat-status {seat_id} | grep /sys/devices"], "get_devices_by_seat")
        if output is None:
            return []
        return DevicesExtractor(output).extract_devices()

    def add_device_to_seat(self, seat: Seat, device: Device) -> None:
        self.shellRun(["loginctl", "attach", seat.seat_id, device.path], "add_device_to_seat")

    def remove_device_from_seat(self, seat: Seat, device_path: str) -> None:
        self.shellRun(["loginctl", "detach", device_path], "remove_device_from_seat")

    def attach_session_to_seat(self, seat: Seat, session: Session) -> None:
        self.shellRun(["loginctl", "attach", seat.seat_id, session.session_id], "attach_session_to_seat")

    def detach_session_from_seat(self, seat: Seat, session_id: str) -> None:
        self.shellRun(["loginctl", "terminate-session", session_id], "detach_session_from_seat")

    def add_seat(self, device_path: str) -> None:
        seat_id = "seat"+str(len(self.get_seats())+1)
        self.shellRun(["loginctl", "attach",seat_id, device_path], "add_seat")

    def remove_seat(self, seat_id: str) -> None:
        for device in self.get_devices_by_seat(seat_id):
            self.shellRun(["loginctl", "detach", device.path], "remove_seat")

    def flush_all_devices(self) -> None:
        self.shellRun(["loginctl", "flush-devices"], "flush_all_devices")

    def get_parent_device(self, device_path: str) -> Optional[Device]:
        devices = self.get_all_devices()
        target = next((d for d in devices if d.path == device_path), None)
        if not target or not target.parent_path:
            return None
        return next((d for d in devices if d.path == target.parent_path), None)

    def get_children_devices(self, device_children: List[str]) -> List[Device]:
        return [d for d in self.get_all_devices() if d.path in device_children]

    def get_device_seat(self, device_path: str) -> Optional[str]:
        for seat in self.get_seats():
            for d in seat.devices:
                if d.path == device_path:
                    return seat.seat_id
        return None
