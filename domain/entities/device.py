
class Device:
    """
    Lightweight representation of a device associated with a seat.
    This should ideally come from a Device entity or factory.
    """
    def __init__(self, path: str, type_: str, name: str):
        self.path = path                # sysfs path (e.g. /sys/devices/...)
        self.type = type_               # input, usb, sound, drm, etc.
        self.name = name                # Human-friendly name (e.g. "Lenovo USB Keyboard")

    def __repr__(self):
        return f"<Device {self.type}: {self.name}>"



