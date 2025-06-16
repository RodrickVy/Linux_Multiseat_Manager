from typing import List

from model.data.device_info import DeviceInfo


class Device:
    """
    Lightweight representation of a device associated with a seat.
    This should ideally come from a Device entity or factory.
    """
    def __init__(self, path: str, type_: str, name: str, parent_path: str, children:List[str]=None,device_information:List[DeviceInfo]=[] ):
        if children is None:
            children = []
        self.path = path                # sysfs path (e.g. /sys/devices/...)
        self.type = type_               # input, usb, sound, drm, etc.
        self.name = name    # Human-friendly name (e.g. "Lenovo USB Keyboard")
        self.children = children   # A list of device paths of the devices that are children to this device
        self.parent_path = parent_path  # the path to this devices parent if any
        self.device_information = device_information # a list of information particular to this device





