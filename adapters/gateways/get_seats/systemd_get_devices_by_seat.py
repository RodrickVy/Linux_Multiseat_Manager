import subprocess
from typing import List
from domain.entities.device import Device
import os


def systemd_get_devices_by_seat(seat_id: str) -> List[Device]:
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
