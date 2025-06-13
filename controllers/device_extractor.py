import os
import re
from typing import List, Optional
from model.data.device import Device


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

            # Determine children (look ahead)
            children_paths = self._collect_children(lines, i, indent_level)

            # Create device object
            device = Device(
                path=path,
                type_=type_,
                name=name,
                parent_path=parent_path,
                children=children_paths
            )
            devices.append(device)
            stack.append((indent_level, path))

        return devices

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
