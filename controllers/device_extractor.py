import os
import re
from typing import List, Optional
from model.data.device import Device
from model.data.device_info import DeviceInfo


class DevicesExtractor:
    """
    Parses tree-indented sysfs device output and returns Device objects with hierarchy metadata.
    """

    def __init__(self, raw_output: str):
        self.raw_output = raw_output

    def extract_devices(self) -> List[Device]:
        lines = self.raw_output.strip().splitlines()
        devices = []
        stack = []  # (indent_level, device_path)

        # Step 1: First parse all devices, set parent_path
        for i, line in enumerate(lines):
            path = self._extract_path(line)
            if not path:
                continue

            indent_level = self._count_indent(line)
            name = os.path.basename(path)
            type_ = self._infer_device_type(path)

            # Determine parent
            parent_path = None
            while stack and stack[-1][0] >= indent_level:
                stack.pop()
            if stack:
                parent_path = stack[-1][1]

            _device_info: List[DeviceInfo] = self.get_device_info(path)
            device = Device(
                path=path,
                type_=type_,
                name=name,
                parent_path=parent_path,
                children=[] , # We'll fill this later
                device_information= _device_info

            )

            devices.append(device)
            stack.append((indent_level, path))

        # Step 2: Build a mapping from path → device
        device_map = {d.path: d for d in devices}

        # Step 3: Fill in direct children
        for device in devices:
            if device.parent_path and device.parent_path in device_map:
                parent = device_map[device.parent_path]
                parent.children.append(device.path)

        # Step 4: Return deduplicated list of devices
        return list(device_map.values())

    def _extract_path(self, line: str) -> Optional[str]:
        match = re.search(r"/sys/devices[^\s]*", line)
        return match.group(0) if match else None

    def _count_indent(self, line: str) -> int:
        return len(line) - len(line.lstrip(" │├─└"))

    def _collect_children(self, lines: List[str], start_index: int, current_indent: int) -> List[str]:
        children = []
        for line in lines[start_index + 1:]:
            if not line.strip():
                continue
            indent = self._count_indent(line)
            if indent <= current_indent:
                break
            path = self._extract_path(line)
            if path:
                children.append(path)
        return children

    def _infer_device_type(self, path: str) -> str:
        if "input" in path:
            return "input"
        elif "usb" in path:
            return "usb"
        elif "sound" in path:
            return "sound"
        elif "drm" in path:
            return "drm"
        elif "graphics" in path:
            return "graphics"
        elif "misc" in path:
            return "misc"
        else:
            return "unknown"

    def get_device_info(self,path: str) -> List[DeviceInfo]:
        device_info_list = []

        if not os.path.isdir(path):
            return device_info_list  # Path doesn't exist or isn't a directory

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().strip()
                    context = filename.replace('_', ' ').title()
                    device_info = DeviceInfo(path=path, info=content, context=context)
                    device_info_list.append(device_info)
                except Exception as e:
                    # Skip unreadable files silently or log if needed
                    continue

        return device_info_list